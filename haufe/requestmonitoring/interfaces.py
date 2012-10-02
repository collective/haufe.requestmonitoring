from zope.interface import Interface, Attribute


class ITicket(Interface):
    """identifying ticket information."""
    id = Attribute("unique ticket id (an integer)")
    time = Attribute("ticket creation time (an integer; seconds since epoch)")
    
    
class IInfo(Interface):
    """information.
    
    Probably this interface should be moved elsewhere
    """
    
    def __str__():
        """the readable information"""
        
        
class IAdditionalInfo(IInfo):
    """set and get additional info.
    
    Almost surely, this interface should be moved elsewhere.
    """
    
    def set(info):
        """set as additional information."""
        
        
class IStatus(Interface):
    """the status (usually of a response)."""
    def __int__():
        """the status code."""
        
        
class ISuccessFull(Interface):
    """was it successful (usually a response)."""
    def __nonzero__():
        """was successful."""
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
