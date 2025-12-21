"""
PwnDoc API Client - HTTP client for PwnDoc REST API.

Handles authentication, rate limiting, retries, and all API endpoints.
"""

import logging
import time
from collections import deque
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, cast

import httpx  # type: ignore[import-not-found]

from .config import Config

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple sliding window rate limiter."""

    def __init__(self, max_requests: int, period: int):
        self.max_requests = max_requests
        self.period = period
        self.requests: deque = deque()

    def acquire(self) -> bool:
        """Try to acquire a request slot."""
        now = time.time()

        # Remove old requests outside the window
        while self.requests and self.requests[0] < now - self.period:
            self.requests.popleft()

        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False

    def wait_time(self) -> float:
        """Time to wait before next request is available."""
        if len(self.requests) < self.max_requests:
            return 0.0
        return float(self.requests[0]) + self.period - time.time()


class PwnDocError(Exception):
    """Base exception for PwnDoc API errors."""

    pass


class AuthenticationError(PwnDocError):
    """Authentication failed."""

    pass


class RateLimitError(PwnDocError):
    """Rate limit exceeded."""

    pass


class NotFoundError(PwnDocError):
    """Resource not found."""

    pass


class PwnDocClient:
    """
    HTTP client for PwnDoc REST API.

    Features:
    - Automatic authentication and token refresh
    - Rate limiting
    - Automatic retries with exponential backoff
    - Connection pooling
    - Comprehensive error handling

    Example:
        >>> client = PwnDocClient(config)
        >>> audits = client.list_audits()
        >>> audit = client.get_audit("507f1f77bcf86cd799439011")
    """

    def __init__(
        self,
        config: Optional[Config] = None,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        verify_ssl: bool = True,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        rate_limit_requests: int = 100,
        rate_limit_period: int = 60,
    ):
        """
        Initialize PwnDoc client.

        Args:
            config: Configuration object (if provided, other params are ignored)
            url: PwnDoc server URL
            username: Username for authentication
            password: Password for authentication
            token: Pre-authenticated JWT token
            verify_ssl: Verify SSL certificates
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            retry_delay: Delay between retries
            rate_limit_requests: Max requests per period
            rate_limit_period: Rate limit period in seconds
        """
        # If config provided, use it; otherwise create from parameters
        if config is not None:
            self.config = config
        else:
            self.config = Config(
                url=url or "",
                username=username or "",
                password=password or "",
                token=token or "",
                verify_ssl=verify_ssl,
                timeout=timeout,
                max_retries=max_retries,
                retry_delay=retry_delay,
                rate_limit_requests=rate_limit_requests,
                rate_limit_period=rate_limit_period,
            )

        self.base_url = self.config.url.rstrip("/")
        self._token: Optional[str] = self.config.token or None
        self._token_expires: Optional[datetime] = None
        self._refresh_token: Optional[str] = None

        self.rate_limiter = RateLimiter(
            self.config.rate_limit_requests, self.config.rate_limit_period
        )

        # Configure HTTP client
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl,
            follow_redirects=True,
        )

        logger.debug(f"PwnDocClient initialized for {self.base_url}")

    @classmethod
    def from_config(cls, config: Config) -> "PwnDocClient":
        """
        Create client from config object.

        Args:
            config: Configuration object

        Returns:
            PwnDocClient instance

        Example:
            >>> config = Config(url="https://pwndoc.com", token="...")
            >>> client = PwnDocClient.from_config(config)
        """
        return cls(config=config)

    @property
    def url(self) -> str:
        """Get the base URL."""
        return self.base_url

    @property
    def token(self) -> Optional[str]:
        """Get the current token."""
        return self._token

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._client.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        """Close the HTTP client (async)."""
        self._client.close()

    async def _ensure_token(self):
        """Ensure we have a valid authentication token (async wrapper)."""
        if not self.is_authenticated:
            self.authenticate()

    async def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to PwnDoc server.

        Returns:
            Dict with status and connection info

        Example:
            >>> result = await client.test_connection()
            >>> if result["status"] == "ok":
            ...     print(f"Connected as {result['user']}")
        """
        try:
            # Try to ensure token (async for test compatibility)
            await self._ensure_token()

            # Get current user to verify connection
            user_data = self.get_current_user()

            # Handle both sync and async mocked returns
            if hasattr(user_data, "__await__"):
                user_data = await user_data

            # Extract username from response (handle both direct and nested format)
            if isinstance(user_data, dict):
                if "datas" in user_data:
                    username = user_data.get("datas", {}).get("username", "unknown")
                else:
                    username = user_data.get("username", "unknown")
            else:
                username = "unknown"

            return {
                "status": "ok",
                "user": username,
                "url": self.base_url,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "url": self.base_url,
            }

    @property
    def is_authenticated(self) -> bool:
        """Check if client has valid authentication."""
        if not self._token:
            return False
        if self._token_expires and datetime.now() >= self._token_expires:
            return False
        return True

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def authenticate(self) -> bool:
        """
        Authenticate with PwnDoc and obtain JWT token.

        Authentication priority (when multiple methods configured):
        1. Username/Password (preferred - automatic token refresh)
        2. Pre-configured Token (fallback - requires manual renewal)

        Returns:
            bool: True if authentication succeeded

        Raises:
            AuthenticationError: If authentication fails
        """
        # Prefer username/password over token (automatic refresh vs manual renewal)
        if self.config.username and self.config.password:
            try:
                response = self._client.post(
                    "/api/users/login",
                    json={
                        "username": self.config.username,
                        "password": self.config.password,
                    },
                    headers={"Content-Type": "application/json"},
                )

                if response.status_code == 200:
                    data = response.json()
                    self._token = data.get("datas", {}).get("token")

                    # Extract refresh token from cookies if present
                    if "refreshToken" in response.cookies:
                        self._refresh_token = response.cookies["refreshToken"]

                    # Set token expiry (default 1 hour)
                    self._token_expires = datetime.now() + timedelta(hours=1)

                    logger.info("Authentication successful via username/password")
                    return True
                else:
                    raise AuthenticationError(
                        f"Authentication failed: {response.status_code} - {response.text}"
                    )
            except httpx.RequestError as e:
                raise AuthenticationError(f"Connection error: {e}")

        # Fallback to pre-configured token if no username/password
        if self.config.token:
            self._token = self.config.token
            logger.info("Using pre-configured token (no automatic refresh)")
            return True

        raise AuthenticationError("No credentials configured (provide username/password or token)")

    def refresh_authentication(self) -> bool:
        """Refresh the authentication token."""
        if self._refresh_token:
            try:
                response = self._client.get(
                    "/api/users/refreshtoken",
                    cookies={"refreshToken": self._refresh_token},
                )
                if response.status_code == 200:
                    data = response.json()
                    self._token = data.get("datas", {}).get("token")
                    self._token_expires = datetime.now() + timedelta(hours=1)
                    logger.debug("Token refreshed")
                    return True
            except Exception as e:
                logger.warning(f"Token refresh failed: {e}")

        # Fall back to full authentication
        return self.authenticate()

    def _ensure_authenticated(self):
        """Ensure we have valid authentication."""
        if not self.is_authenticated:
            if self._refresh_token:
                self.refresh_authentication()
            else:
                self.authenticate()

    def _wait_for_rate_limit(self):
        """Wait if rate limited."""
        while not self.rate_limiter.acquire():
            wait_time = self.rate_limiter.wait_time()
            logger.debug(f"Rate limited, waiting {wait_time:.2f}s")
            time.sleep(wait_time)

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an API request with retries and error handling.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional request arguments

        Returns:
            Parsed JSON response

        Raises:
            PwnDocError: On API errors
        """
        self._ensure_authenticated()
        self._wait_for_rate_limit()

        url = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        headers = self._get_headers()
        headers.update(kwargs.pop("headers", {}))

        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                response = self._client.request(method, url, headers=headers, **kwargs)

                # Handle response
                if response.status_code == 200:
                    try:
                        return cast(Dict[str, Any], response.json())
                    except Exception:
                        return {"raw": response.text}
                elif response.status_code == 401:
                    # Token expired, try to refresh
                    self.refresh_authentication()
                    headers["Authorization"] = f"Bearer {self._token}"
                    continue
                elif response.status_code == 404:
                    raise NotFoundError(f"Resource not found: {endpoint}")
                elif response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    raise RateLimitError(f"Rate limited, retry after {retry_after}s")
                else:
                    raise PwnDocError(f"API error: {response.status_code} - {response.text}")

            except httpx.RequestError as e:
                last_error = e
                logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (2**attempt))

        raise PwnDocError(f"Request failed after {self.config.max_retries} retries: {last_error}")

    def _get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make GET request."""
        return self._request("GET", endpoint, **kwargs)

    def _post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make POST request."""
        return self._request("POST", endpoint, **kwargs)

    def _put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make PUT request."""
        return self._request("PUT", endpoint, **kwargs)

    def _delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)

    # =========================================================================
    # AUDIT ENDPOINTS
    # =========================================================================

    def list_audits(self, finding_title: Optional[str] = None) -> List[Dict]:
        """List all audits, optionally filtered by finding title."""
        response = self._get("/api/audits")
        audits = response.get("datas", [])

        if finding_title:
            filtered = []
            for audit in audits:
                for finding in audit.get("findings", []):
                    if finding_title.lower() in finding.get("title", "").lower():
                        filtered.append(audit)
                        break
            return filtered
        return audits

    def get_audit(self, audit_id: str) -> Dict:
        """Get detailed audit information."""
        response = self._get(f"/api/audits/{audit_id}")
        return response.get("datas", {})

    def get_audit_general(self, audit_id: str) -> Dict:
        """Get audit general information."""
        response = self._get(f"/api/audits/{audit_id}/general")
        return response.get("datas", {})

    def create_audit(self, name: str, language: str, audit_type: str, **kwargs) -> Dict:
        """Create a new audit."""
        data = {"name": name, "language": language, "auditType": audit_type, **kwargs}
        response = self._post("/api/audits", json=data)
        return response.get("datas", {})

    def update_audit_general(self, audit_id: str, **kwargs) -> Dict:
        """Update audit general information."""
        response = self._put(f"/api/audits/{audit_id}/general", json=kwargs)
        return response.get("datas", {})

    def delete_audit(self, audit_id: str) -> bool:
        """Delete an audit."""
        self._delete(f"/api/audits/{audit_id}")
        return True

    def generate_report(self, audit_id: str) -> bytes:
        """Generate and download audit report."""
        self._ensure_authenticated()
        response = self._client.get(
            f"/api/audits/{audit_id}/generate",
            headers=self._get_headers(),
        )
        if response.status_code == 200:
            return response.content
        raise PwnDocError(f"Report generation failed: {response.status_code}")

    def get_audit_network(self, audit_id: str) -> Dict:
        """Get audit network information."""
        response = self._get(f"/api/audits/{audit_id}/network")
        return response.get("datas", {})

    def update_audit_network(self, audit_id: str, network_data: Dict) -> Dict:
        """Update audit network information."""
        response = self._put(f"/api/audits/{audit_id}/network", json=network_data)
        return response.get("datas", {})

    def toggle_audit_approval(self, audit_id: str) -> Dict:
        """Toggle audit approval status."""
        response = self._put(f"/api/audits/{audit_id}/toggleApproval")
        return response.get("datas", {})

    def update_review_status(self, audit_id: str, state: bool) -> Dict:
        """Update audit review ready status."""
        response = self._put(f"/api/audits/{audit_id}/updateReadyForReview", json={"state": state})
        return response.get("datas", {})

    # =========================================================================
    # FINDING ENDPOINTS
    # =========================================================================

    def get_findings(self, audit_id: str) -> List[Dict]:
        """Get all findings for an audit."""
        response = self._get(f"/api/audits/{audit_id}/findings")
        return response.get("datas", [])

    def get_finding(self, audit_id: str, finding_id: str) -> Dict:
        """Get specific finding details."""
        response = self._get(f"/api/audits/{audit_id}/findings/{finding_id}")
        return response.get("datas", {})

    def create_finding(self, audit_id: str, **kwargs) -> Dict:
        """Create a new finding."""
        response = self._post(f"/api/audits/{audit_id}/findings", json=kwargs)
        return response.get("datas", {})

    def update_finding(self, audit_id: str, finding_id: str, **kwargs) -> Dict:
        """Update an existing finding."""
        response = self._put(f"/api/audits/{audit_id}/findings/{finding_id}", json=kwargs)
        return response.get("datas", {})

    def delete_finding(self, audit_id: str, finding_id: str) -> bool:
        """Delete a finding."""
        self._delete(f"/api/audits/{audit_id}/findings/{finding_id}")
        return True

    def sort_findings(self, audit_id: str, finding_order: List[str]) -> Dict:
        """Reorder findings in an audit."""
        response = self._put(
            f"/api/audits/{audit_id}/sortFindings", json={"findings": finding_order}
        )
        return response.get("datas", {})

    def move_finding(self, audit_id: str, finding_id: str, destination_audit_id: str) -> Dict:
        """Move finding to another audit."""
        response = self._post(
            f"/api/audits/{audit_id}/findings/{finding_id}/move/{destination_audit_id}"
        )
        return response.get("datas", {})

    # =========================================================================
    # CLIENT & COMPANY ENDPOINTS
    # =========================================================================

    def list_clients(self) -> List[Dict]:
        """List all clients."""
        response = self._get("/api/clients")
        return response.get("datas", [])

    def create_client(self, **kwargs) -> Dict:
        """Create a new client."""
        response = self._post("/api/clients", json=kwargs)
        return response.get("datas", {})

    def update_client(self, client_id: str, **kwargs) -> Dict:
        """Update a client."""
        response = self._put(f"/api/clients/{client_id}", json=kwargs)
        return response.get("datas", {})

    def delete_client(self, client_id: str) -> bool:
        """Delete a client."""
        self._delete(f"/api/clients/{client_id}")
        return True

    def list_companies(self) -> List[Dict]:
        """List all companies."""
        response = self._get("/api/companies")
        return response.get("datas", [])

    def create_company(self, **kwargs) -> Dict:
        """Create a new company."""
        response = self._post("/api/companies", json=kwargs)
        return response.get("datas", {})

    def update_company(self, company_id: str, **kwargs) -> Dict:
        """Update a company."""
        response = self._put(f"/api/companies/{company_id}", json=kwargs)
        return response.get("datas", {})

    def delete_company(self, company_id: str) -> bool:
        """Delete a company."""
        self._delete(f"/api/companies/{company_id}")
        return True

    # =========================================================================
    # VULNERABILITY TEMPLATE ENDPOINTS
    # =========================================================================

    def list_vulnerabilities(self) -> List[Dict]:
        """List all vulnerability templates."""
        response = self._get("/api/vulnerabilities")
        return response.get("datas", [])

    def get_vulnerabilities_by_locale(self, locale: str = "en") -> List[Dict]:
        """Get vulnerability templates for a locale."""
        response = self._get(f"/api/vulnerabilities/{locale}")
        return response.get("datas", [])

    def create_vulnerability(self, **kwargs) -> Dict:
        """Create a vulnerability template."""
        response = self._post("/api/vulnerabilities", json=kwargs)
        return response.get("datas", {})

    def update_vulnerability(self, vuln_id: str, **kwargs) -> Dict:
        """Update a vulnerability template."""
        response = self._put(f"/api/vulnerabilities/{vuln_id}", json=kwargs)
        return response.get("datas", {})

    def delete_vulnerability(self, vuln_id: str) -> bool:
        """Delete a vulnerability template."""
        self._delete(f"/api/vulnerabilities/{vuln_id}")
        return True

    def bulk_delete_vulnerabilities(self, vuln_ids: List[str]) -> bool:
        """Bulk delete vulnerability templates."""
        self._delete("/api/vulnerabilities", json={"vulnIds": vuln_ids})
        return True

    def export_vulnerabilities(self) -> Dict:
        """Export all vulnerability templates."""
        response = self._get("/api/vulnerabilities/export")
        return response.get("datas", {})

    def create_vulnerability_from_finding(self, **kwargs) -> Dict:
        """Create vulnerability template from finding."""
        response = self._post("/api/vulnerabilities/from-finding", json=kwargs)
        return response.get("datas", {})

    # =========================================================================
    # USER ENDPOINTS
    # =========================================================================

    def list_users(self) -> List[Dict]:
        """List all users (admin only)."""
        response = self._get("/api/users")
        return response.get("datas", [])

    def get_user(self, username: str) -> Dict:
        """Get user by username."""
        response = self._get(f"/api/users/{username}")
        return response.get("datas", {})

    def get_current_user(self) -> Dict:
        """Get current authenticated user."""
        response = self._get("/api/users/me")
        return response.get("datas", {})

    def create_user(self, **kwargs) -> Dict:
        """Create a new user (admin only)."""
        response = self._post("/api/users", json=kwargs)
        return response.get("datas", {})

    def update_user(self, user_id: str, **kwargs) -> Dict:
        """Update a user (admin only)."""
        response = self._put(f"/api/users/{user_id}", json=kwargs)
        return response.get("datas", {})

    def update_current_user(self, **kwargs) -> Dict:
        """Update current user profile."""
        response = self._put("/api/users/me", json=kwargs)
        return response.get("datas", {})

    def list_reviewers(self) -> List[Dict]:
        """List all reviewers."""
        response = self._get("/api/users/reviewers")
        return response.get("datas", [])

    # =========================================================================
    # TEMPLATE & SETTINGS ENDPOINTS
    # =========================================================================

    def list_templates(self) -> List[Dict]:
        """List report templates."""
        response = self._get("/api/templates")
        return response.get("datas", [])

    def create_template(self, name: str, ext: str, file_content: str) -> Dict:
        """Create/upload a report template."""
        response = self._post(
            "/api/templates", json={"name": name, "ext": ext, "file": file_content}
        )
        return response.get("datas", {})

    def update_template(self, template_id: str, **kwargs) -> Dict:
        """Update a template."""
        response = self._put(f"/api/templates/{template_id}", json=kwargs)
        return response.get("datas", {})

    def delete_template(self, template_id: str) -> bool:
        """Delete a template."""
        self._delete(f"/api/templates/{template_id}")
        return True

    def download_template(self, template_id: str) -> bytes:
        """Download a template file."""
        self._ensure_authenticated()
        response = self._client.get(
            f"/api/templates/download/{template_id}",
            headers=self._get_headers(),
        )
        return response.content

    def get_settings(self) -> Dict:
        """Get system settings."""
        response = self._get("/api/settings")
        return response.get("datas", {})

    def get_public_settings(self) -> Dict:
        """Get public settings."""
        response = self._get("/api/settings/public")
        return response.get("datas", {})

    def update_settings(self, settings: Dict) -> Dict:
        """Update system settings."""
        response = self._put("/api/settings", json=settings)
        return response.get("datas", {})

    # =========================================================================
    # DATA TYPE ENDPOINTS
    # =========================================================================

    def list_languages(self) -> List[Dict]:
        """List all languages."""
        response = self._get("/api/data/languages")
        return response.get("datas", [])

    def list_audit_types(self) -> List[Dict]:
        """List all audit types."""
        response = self._get("/api/data/audit-types")
        return response.get("datas", [])

    def list_vulnerability_types(self) -> List[Dict]:
        """List all vulnerability types."""
        response = self._get("/api/data/vulnerability-types")
        return response.get("datas", [])

    def list_vulnerability_categories(self) -> List[Dict]:
        """List all vulnerability categories."""
        response = self._get("/api/data/vulnerability-categories")
        return response.get("datas", [])

    def list_sections(self) -> List[Dict]:
        """List all section definitions."""
        response = self._get("/api/data/sections")
        return response.get("datas", [])

    def list_custom_fields(self) -> List[Dict]:
        """List all custom field definitions."""
        response = self._get("/api/data/custom-fields")
        return response.get("datas", [])

    def list_roles(self) -> List[Dict]:
        """List all user roles."""
        response = self._get("/api/data/roles")
        return response.get("datas", [])

    # =========================================================================
    # IMAGE ENDPOINTS
    # =========================================================================

    def get_image(self, image_id: str) -> Dict:
        """Get image metadata."""
        response = self._get(f"/api/images/{image_id}")
        return response.get("datas", {})

    def download_image(self, image_id: str) -> bytes:
        """Download an image file."""
        self._ensure_authenticated()
        response = self._client.get(
            f"/api/images/download/{image_id}",
            headers=self._get_headers(),
        )
        return response.content

    def upload_image(self, audit_id: str, name: str, value: str) -> Dict:
        """Upload an image."""
        response = self._post(
            "/api/images", json={"auditId": audit_id, "name": name, "value": value}
        )
        return response.get("datas", {})

    def delete_image(self, image_id: str) -> bool:
        """Delete an image."""
        self._delete(f"/api/images/{image_id}")
        return True

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics."""
        # Aggregate statistics from multiple endpoints
        stats = {
            "audits": len(self.list_audits()),
            "clients": len(self.list_clients()),
            "companies": len(self.list_companies()),
            "vulnerability_templates": len(self.list_vulnerabilities()),
            "users": len(self.list_users()),
        }
        return stats

    def search_findings(
        self,
        title: Optional[str] = None,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict]:
        """Search findings across all audits."""
        results = []
        audits = self.list_audits()

        for audit in audits:
            findings = self.get_findings(audit["_id"])
            for finding in findings:
                match = True

                if title and title.lower() not in finding.get("title", "").lower():
                    match = False
                if category and category.lower() != finding.get("category", "").lower():
                    match = False
                if severity:
                    # Map CVSS to severity
                    cvss = finding.get("cvssv3", "")
                    if severity.lower() == "critical" and not (
                        cvss and float(cvss.split("/")[0]) >= 9.0
                    ):
                        match = False
                    elif severity.lower() == "high" and not (
                        cvss and 7.0 <= float(cvss.split("/")[0]) < 9.0
                    ):
                        match = False

                if match:
                    finding["_audit_id"] = audit["_id"]
                    finding["_audit_name"] = audit.get("name", "")
                    results.append(finding)

        return results

    def get_all_findings_with_context(
        self, include_failed: bool = False, exclude_categories: Optional[List[str]] = None
    ) -> List[Dict]:
        """Get all findings with full audit context."""
        exclude_categories = exclude_categories or []
        if not include_failed:
            exclude_categories.append("Failed")

        results = []
        audits = self.list_audits()

        for audit in audits:
            audit_detail = self.get_audit(audit["_id"])
            findings = self.get_findings(audit["_id"])

            for finding in findings:
                if finding.get("category") in exclude_categories:
                    continue

                # Add audit context
                finding["audit"] = {
                    "_id": audit["_id"],
                    "name": audit.get("name"),
                    "company": audit_detail.get("company", {}).get("name"),
                    "client": audit_detail.get("client", {}).get("email"),
                    "date_start": audit_detail.get("date_start"),
                    "date_end": audit_detail.get("date_end"),
                    "scope": audit_detail.get("scope", []),
                }
                results.append(finding)

        return results
