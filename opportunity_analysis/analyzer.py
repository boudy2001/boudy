"""Lost Opportunity Analyzer - AI-powered post-mortem analysis engine"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class ImprovementPriority(str, Enum):
    """Priority levels for improvement recommendations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ProcessMetric:
    """Captures process timing and performance data"""
    submission_date: str
    approval_date: Optional[str]
    revision_count: int
    approval_duration_days: int
    revision_cycle_duration_days: int
    total_cycle_time_days: int


@dataclass
class ImprovementRecommendation:
    """AI-generated improvement recommendation"""
    title: str
    description: str
    priority: ImprovementPriority
    estimated_impact: str
    implementation_effort: str
    related_factors: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "estimated_impact": self.estimated_impact,
            "implementation_effort": self.implementation_effort,
            "related_factors": self.related_factors,
            "confidence_score": self.confidence_score,
        }


@dataclass
class OpportunityAnalysisResult:
    """Complete analysis result for a lost opportunity"""
    opportunity_id: str
    opportunity_name: str
    loss_date: str
    client_name: str
    rejection_reason: str
    competitor_info: Optional[str]
    manual_input_provided: bool
    process_metrics: Optional[ProcessMetric]
    key_findings: List[str] = field(default_factory=list)
    improvement_recommendations: List[ImprovementRecommendation] = field(default_factory=list)
    analysis_timestamp: str = ""
    ai_model_version: str = "1.0"
    analysis_completeness: float = 1.0  # 0.0-1.0, indicates if full data was available
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "opportunity_id": self.opportunity_id,
            "opportunity_name": self.opportunity_name,
            "loss_date": self.loss_date,
            "client_name": self.client_name,
            "rejection_reason": self.rejection_reason,
            "competitor_info": self.competitor_info,
            "manual_input_provided": self.manual_input_provided,
            "process_metrics": self.process_metrics.__dict__ if self.process_metrics else None,
            "key_findings": self.key_findings,
            "improvement_recommendations": [r.to_dict() for r in self.improvement_recommendations],
            "analysis_timestamp": self.analysis_timestamp,
            "ai_model_version": self.ai_model_version,
            "analysis_completeness": self.analysis_completeness,
        }


class OpportunityAnalyzer:
    """AI-powered lost opportunity post-mortem analysis"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the opportunity analyzer
        
        Args:
            config: Configuration dictionary for analyzer settings
        """
        self.config = config or {}
        self.enable_auto_partial_analysis = self.config.get('auto_partial_analysis', True)
        logger.info("OpportunityAnalyzer initialized")
    
    def analyze_lost_opportunity(self, opportunity_id: str, loss_report: Dict[str, Any],
                                process_data: Optional[Dict[str, Any]] = None) -> OpportunityAnalysisResult:
        """Analyze a lost opportunity and generate improvement recommendations
        
        Args:
            opportunity_id: Unique identifier for the opportunity
            loss_report: Manual input report with client feedback and rejection reasons
            process_data: Automatically extracted process metrics (optional)
            
        Returns:
            OpportunityAnalysisResult with findings and recommendations
        """
        logger.info(f"Analyzing lost opportunity {opportunity_id}")
        
        manual_input_provided = bool(loss_report)
        process_metrics = self._extract_process_metrics(process_data) if process_data else None
        
        # Analyze rejection reasons and client feedback
        key_findings = self._extract_key_findings(loss_report, process_metrics)
        
        # Generate improvement recommendations using AI
        recommendations = self._generate_recommendations(loss_report, key_findings, process_metrics)
        
        # Calculate analysis completeness score
        completeness = self._calculate_completeness(manual_input_provided, process_metrics is not None)
        
        analysis = OpportunityAnalysisResult(
            opportunity_id=opportunity_id,
            opportunity_name=loss_report.get('opportunity_name', opportunity_id),
            loss_date=loss_report.get('loss_date', ''),
            client_name=loss_report.get('client_name', ''),
            rejection_reason=loss_report.get('rejection_reason', ''),
            competitor_info=loss_report.get('competitor_info'),
            manual_input_provided=manual_input_provided,
            process_metrics=process_metrics,
            key_findings=key_findings,
            improvement_recommendations=recommendations,
            analysis_timestamp=datetime.utcnow().isoformat(),
            analysis_completeness=completeness,
        )
        
        logger.info(f"Analysis complete for opportunity {opportunity_id}")
        return analysis
    
    def analyze_with_auto_partial(self, opportunity_id: str,
                                 process_data: Dict[str, Any]) -> OpportunityAnalysisResult:
        """Perform automatic partial analysis using only process data
        
        This method allows analysis to proceed even when manual input is unavailable,
        ensuring continuous learning is never blocked.
        
        Args:
            opportunity_id: Unique identifier for the opportunity
            process_data: Automatically extracted process metrics
            
        Returns:
            OpportunityAnalysisResult with partial analysis
        """
        logger.info(f"Performing partial auto-analysis for {opportunity_id}")
        
        process_metrics = self._extract_process_metrics(process_data)
        
        # Generate findings from process data alone
        key_findings = self._extract_key_findings({}, process_metrics)
        
        # Generate recommendations based on process patterns
        recommendations = self._generate_recommendations({}, key_findings, process_metrics)
        
        analysis = OpportunityAnalysisResult(
            opportunity_id=opportunity_id,
            opportunity_name=process_data.get('opportunity_name', opportunity_id),
            loss_date=process_data.get('loss_date', ''),
            client_name=process_data.get('client_name', ''),
            rejection_reason="Unknown (auto-analysis)",
            competitor_info=None,
            manual_input_provided=False,
            process_metrics=process_metrics,
            key_findings=key_findings,
            improvement_recommendations=recommendations,
            analysis_timestamp=datetime.utcnow().isoformat(),
            analysis_completeness=0.6,  # Lower completeness without manual input
        )
        
        logger.info(f"Partial analysis complete for {opportunity_id}")
        return analysis
    
    def _extract_process_metrics(self, process_data: Dict[str, Any]) -> ProcessMetric:
        """Extract process metrics from system data
        
        Args:
            process_data: Process data dictionary
            
        Returns:
            ProcessMetric object
        """
        return ProcessMetric(
            submission_date=process_data.get('submission_date', ''),
            approval_date=process_data.get('approval_date'),
            revision_count=process_data.get('revision_count', 0),
            approval_duration_days=process_data.get('approval_duration_days', 0),
            revision_cycle_duration_days=process_data.get('revision_cycle_duration_days', 0),
            total_cycle_time_days=process_data.get('total_cycle_time_days', 0),
        )
    
    def _extract_key_findings(self, loss_report: Dict[str, Any],
                             process_metrics: Optional[ProcessMetric]) -> List[str]:
        """Extract key findings from loss report and process metrics
        
        Args:
            loss_report: Loss report data
            process_metrics: Process metrics object
            
        Returns:
            List of key finding strings
        """
        # TODO: Implement AI-powered finding extraction
        findings = []
        
        if loss_report:
            if rejection_reason := loss_report.get('rejection_reason'):
                findings.append(f"Client rejection reason: {rejection_reason}")
            if competitor_info := loss_report.get('competitor_info'):
                findings.append(f"Competitor intelligence: {competitor_info}")
        
        if process_metrics:
            if process_metrics.revision_count > 3:
                findings.append(f"High revision count: {process_metrics.revision_count} revisions")
            if process_metrics.approval_duration_days > 20:
                findings.append(f"Extended approval cycle: {process_metrics.approval_duration_days} days")
        
        return findings
    
    def _generate_recommendations(self, loss_report: Dict[str, Any],
                                 findings: List[str],
                                 process_metrics: Optional[ProcessMetric]) -> List[ImprovementRecommendation]:
        """Generate AI-driven improvement recommendations
        
        Args:
            loss_report: Loss report data
            findings: Key findings list
            process_metrics: Process metrics object
            
        Returns:
            List of ImprovementRecommendation objects
        """
        # TODO: Use LLM to generate contextual improvement recommendations
        recommendations = []
        
        if process_metrics and process_metrics.revision_count > 3:
            recommendations.append(ImprovementRecommendation(
                title="Streamline Contract Review Process",
                description="High revision count suggests contract review process may benefit from clearer initial requirements or pre-review consultation.",
                priority=ImprovementPriority.HIGH,
                estimated_impact="Reduced cycle time, faster client response",
                implementation_effort="Medium",
                confidence_score=0.82,
            ))
        
        return recommendations
    
    def _calculate_completeness(self, has_manual: bool, has_process: bool) -> float:
        """Calculate analysis completeness score
        
        Args:
            has_manual: Whether manual input was provided
            has_process: Whether process metrics are available
            
        Returns:
            Completeness score (0.0-1.0)
        """
        base_score = 0.3  # Minimum completeness
        if has_manual:
            base_score += 0.5
        if has_process:
            base_score += 0.2
        return min(base_score, 1.0)
