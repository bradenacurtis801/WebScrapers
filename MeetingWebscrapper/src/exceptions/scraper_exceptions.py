class FailedInitializationError(Exception):
    """Raised when there's a problem during the initialization process."""

class LoginError(Exception):
    """Raised during login failures."""

class BrowserWindowError(Exception):
    """Raised when there's an issue with the browser window."""
    
class NavigationError(Exception):
    """Raised when navigation to a specific URL fails."""

class LoginFieldNotFoundError(Exception):
    """Raised when login fields cannot be located."""

class LoginActionError(Exception):
    """Raised when an action during the login sequence fails."""
