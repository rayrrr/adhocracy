from datetime import datetime, timedelta

from util import BaseTile

from pylons import request, response, session, tmpl_context as c

from .. import democracy
from .. import helpers as h
from ..auth import authorization as auth
import adhocracy.model as model

class DelegateableTile(BaseTile):
    
    def __init__(self, delegateable):
        self.delegateable = delegateable
        self.__dnode = None
        self.__delegations = None
        self.__num_principals = None
    
    def _dnode(self):
        if not self.__dnode:
            self.__dnode = democracy.DelegationNode(c.user, self.delegateable)
        return self.__dnode
    
    dnode = property(_dnode)
    
    def _delegations(self):
        if not self.__delegations:
            self.__delegations = self.dnode.outbound()
        return self.__delegations
    
    delegations = property(_delegations)
    
    def _num_principals(self):
        if self.__num_principals == None:
            principals = set(map(lambda d: d.principal, 
                                 self.dnode.transitive_inbound()))
            self.__num_principals = len(principals)
        return self.__num_principals
    
    num_principals = property(_num_principals)
    
    def _has_delegated(self):
        return len(self.delegations) > 0
    
    has_delegated = property(_has_delegated)
    
    def _has_overridden(self):
        return False
    
    has_overridden = property(_has_overridden)      
    
    def _latest_revision_time(self):
        time = self.delegateable.find_latest_comment_time()
        if time is None:
            return self.delegateable.create_time
        return time
    
    latest_revision_time = property(_latest_revision_time)
