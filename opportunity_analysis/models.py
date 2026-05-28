"""Data models for lost opportunity analysis"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class LossReport:
    """Structured loss report submitted by BD engineer"""
    opportunity_id: str
    opportunity_name: str
    client_name: str
    loss_date: str
    rejection_reason: str
    client_feedback: str
    competitor_info: Optional[str] = None
    estimated_value: Optional[float] = None
    contract_type: Optional[str] = None
    bd_engineer: Optional[str] = None
    notes: Optional[str] = None
    submission_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'opportunity_id': self.opportunity_id,
            'opportunity_name': self.opportunity_name,
            'client_name': self.client_name,
            'loss_date': self.loss_date,
            'rejection_reason': self.rejection_reason,
            'client_feedback': self.client_feedback,
            'competitor_info': self.competitor_info,
            'estimated_value': self.estimated_value,
            'contract_type': self.contract_type,
            'bd_engineer': self.bd_engineer,
            'notes': self.notes,
            'submission_timestamp': self.submission_timestamp,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LossReport':
        """Create LossReport from dictionary
        
        Args:
            data: Dictionary containing loss report data
            
        Returns:
            LossReport instance
        """
        return cls(
            opportunity_id=data.get('opportunity_id', ''),
            opportunity_name=data.get('opportunity_name', ''),
            client_name=data.get('client_name', ''),
            loss_date=data.get('loss_date', ''),
            rejection_reason=data.get('rejection_reason', ''),
            client_feedback=data.get('client_feedback', ''),
            competitor_info=data.get('competitor_info'),
            estimated_value=data.get('estimated_value'),
            contract_type=data.get('contract_type'),
            bd_engineer=data.get('bd_engineer'),
            notes=data.get('notes'),
            submission_timestamp=data.get('submission_timestamp',
                                        datetime.utcnow().isoformat()),
        )
