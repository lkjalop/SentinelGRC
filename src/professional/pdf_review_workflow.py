"""
PDF Review Workflow with Human-in-the-Loop System
=================================================

Enables expert review and enhancement of AI-generated compliance reports
before delivery to customers. Includes version control, expert comments,
and learning feedback loop.

Author: Sentinel GRC Platform
Version: 1.0.0
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field
import hashlib
import logging

logger = logging.getLogger(__name__)

class ReviewStatus(Enum):
    """PDF review status states"""
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    IN_REVIEW = "in_review"
    CHANGES_REQUESTED = "changes_requested"
    APPROVED = "approved"
    DELIVERED = "delivered"
    ARCHIVED = "archived"

class ExpertiseLevel(Enum):
    """Reviewer expertise levels"""
    JUNIOR = "junior"
    SENIOR = "senior"
    PRINCIPAL = "principal"
    PARTNER = "partner"

@dataclass
class ReviewComment:
    """Expert comment on PDF report"""
    comment_id: str
    reviewer_id: str
    reviewer_name: str
    timestamp: datetime
    section: str  # Which section of PDF
    comment_type: str  # "suggestion", "correction", "insight", "warning"
    comment_text: str
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None

@dataclass
class PDFReviewRequest:
    """Request for human review of PDF report"""
    request_id: str
    draft_pdf_path: str
    customer_name: str
    framework: str
    assessment_date: datetime
    created_at: datetime
    due_date: datetime
    status: ReviewStatus
    assigned_reviewer: Optional[str] = None
    priority: str = "normal"  # "low", "normal", "high", "urgent"
    review_checklist: List[str] = field(default_factory=list)
    comments: List[ReviewComment] = field(default_factory=list)
    version: int = 1
    final_pdf_path: Optional[str] = None
    delivered_at: Optional[datetime] = None
    customer_feedback: Optional[Dict[str, Any]] = None

class PDFReviewWorkflow:
    """
    Manages human-in-the-loop PDF review process
    """
    
    def __init__(self, review_queue_path: str = "data/review_queue"):
        self.review_queue_path = review_queue_path
        self.ensure_directories()
        self.review_queue: List[PDFReviewRequest] = []
        self.load_review_queue()
        
        # Standard review checklist
        self.standard_checklist = [
            "Executive summary accuracy and completeness",
            "Technical findings validity and clarity",
            "Remediation recommendations feasibility",
            "Cost estimates and timeline reasonableness",
            "No sensitive data exposure or PII leakage",
            "Grammar, spelling, and formatting",
            "Compliance matrices completeness",
            "Risk ratings appropriateness",
            "Industry-specific context accuracy",
            "Strategic recommendations alignment"
        ]
        
        # Expert insights prompts
        self.expert_prompts = [
            "Add industry-specific context the customer should know",
            "Include regulatory changes on the horizon",
            "Suggest quick wins for immediate improvement",
            "Identify potential budget or resource constraints",
            "Note any political/organizational considerations",
            "Recommend follow-up services or assessments",
            "Highlight competitive advantages from compliance",
            "Add executive talking points for board presentations"
        ]
    
    def ensure_directories(self):
        """Create necessary directories"""
        directories = [
            self.review_queue_path,
            f"{self.review_queue_path}/drafts",
            f"{self.review_queue_path}/approved",
            f"{self.review_queue_path}/delivered",
            f"{self.review_queue_path}/archive"
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def create_review_request(self, 
                            draft_pdf_path: str,
                            customer_name: str,
                            framework: str,
                            assessment_data: Dict[str, Any],
                            priority: str = "normal",
                            due_in_hours: int = 24) -> PDFReviewRequest:
        """
        Create a new PDF review request and add to queue
        """
        request_id = f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        # Move draft to review queue
        draft_filename = os.path.basename(draft_pdf_path)
        queued_draft_path = f"{self.review_queue_path}/drafts/{request_id}_{draft_filename}"
        
        # Copy draft to queue (in production, would move/copy actual file)
        # For now, just reference the path
        
        review_request = PDFReviewRequest(
            request_id=request_id,
            draft_pdf_path=queued_draft_path,
            customer_name=customer_name,
            framework=framework,
            assessment_date=datetime.now(),
            created_at=datetime.now(),
            due_date=datetime.now() + timedelta(hours=due_in_hours),
            status=ReviewStatus.PENDING_REVIEW,
            priority=priority,
            review_checklist=self.standard_checklist.copy()
        )
        
        # Add to queue
        self.review_queue.append(review_request)
        self.save_review_queue()
        
        # Send notification (in production, would send email/Slack)
        self._notify_reviewers(review_request)
        
        logger.info(f"Created review request {request_id} for {customer_name}")
        return review_request
    
    def assign_reviewer(self, request_id: str, reviewer_id: str) -> bool:
        """Assign a reviewer to a request"""
        request = self.get_request(request_id)
        if not request:
            return False
        
        request.assigned_reviewer = reviewer_id
        request.status = ReviewStatus.IN_REVIEW
        self.save_review_queue()
        
        logger.info(f"Assigned reviewer {reviewer_id} to request {request_id}")
        return True
    
    def add_expert_comment(self, 
                          request_id: str,
                          reviewer_id: str,
                          reviewer_name: str,
                          section: str,
                          comment_type: str,
                          comment_text: str) -> bool:
        """Add expert comment to review"""
        request = self.get_request(request_id)
        if not request:
            return False
        
        comment = ReviewComment(
            comment_id=uuid.uuid4().hex,
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            timestamp=datetime.now(),
            section=section,
            comment_type=comment_type,
            comment_text=comment_text
        )
        
        request.comments.append(comment)
        self.save_review_queue()
        
        logger.info(f"Added comment to request {request_id} by {reviewer_name}")
        return True
    
    def generate_review_interface(self, request_id: str) -> str:
        """Generate HTML interface for reviewing PDF"""
        request = self.get_request(request_id)
        if not request:
            return "<h1>Review request not found</h1>"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>PDF Review - {request.customer_name}</title>
            <style>
                body {{ font-family: 'Inter', -apple-system, sans-serif; margin: 0; }}
                .review-container {{ display: flex; height: 100vh; }}
                .pdf-viewer {{ flex: 1; background: #f5f5f5; }}
                .review-panel {{ width: 400px; background: white; padding: 20px; overflow-y: auto; }}
                .checklist-item {{ padding: 8px; margin: 4px 0; }}
                .checklist-item input {{ margin-right: 8px; }}
                .comment-box {{ width: 100%; min-height: 100px; margin: 10px 0; }}
                .expert-prompt {{ background: #e3f2fd; padding: 10px; margin: 5px 0; border-radius: 4px; }}
                .btn {{ padding: 10px 20px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; }}
                .btn-approve {{ background: #4caf50; color: white; }}
                .btn-changes {{ background: #ff9800; color: white; }}
                .btn-schedule {{ background: #2196f3; color: white; }}
                .priority-{request.priority} {{ color: #ff5722; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="review-container">
                <div class="pdf-viewer">
                    <iframe src="{request.draft_pdf_path}" width="100%" height="100%"></iframe>
                </div>
                
                <div class="review-panel">
                    <h2>Review: {request.customer_name}</h2>
                    <p>Framework: <strong>{request.framework}</strong></p>
                    <p>Priority: <span class="priority-{request.priority}">{request.priority.upper()}</span></p>
                    <p>Due: {request.due_date.strftime('%Y-%m-%d %H:%M')}</p>
                    
                    <h3>Review Checklist</h3>
                    <div class="checklist">
        """
        
        for item in request.review_checklist:
            html += f"""
                        <div class="checklist-item">
                            <input type="checkbox" id="check_{hash(item)}" />
                            <label for="check_{hash(item)}">{item}</label>
                        </div>
            """
        
        html += """
                    </div>
                    
                    <h3>Add Expert Insights</h3>
        """
        
        for prompt in self.expert_prompts:
            html += f"""
                    <div class="expert-prompt">{prompt}</div>
        """
        
        html += f"""
                    <h3>Your Comments</h3>
                    <select id="comment-section">
                        <option>Executive Summary</option>
                        <option>Technical Findings</option>
                        <option>Remediation Plan</option>
                        <option>Cost Analysis</option>
                        <option>Risk Assessment</option>
                        <option>Compliance Matrix</option>
                    </select>
                    
                    <select id="comment-type">
                        <option value="suggestion">Suggestion</option>
                        <option value="correction">Correction</option>
                        <option value="insight">Strategic Insight</option>
                        <option value="warning">Warning</option>
                    </select>
                    
                    <textarea class="comment-box" id="expert-comment" 
                        placeholder="Add your expert insights, industry context, or strategic recommendations...">
                    </textarea>
                    
                    <div class="actions">
                        <button class="btn btn-approve" onclick="approve('{request.request_id}')">
                            ✓ Approve & Send
                        </button>
                        <button class="btn btn-changes" onclick="requestChanges('{request.request_id}')">
                            ↻ Request Changes
                        </button>
                        <button class="btn btn-schedule" onclick="scheduleCall('{request.request_id}')">
                            📞 Schedule Customer Call
                        </button>
                    </div>
                    
                    <h3>Previous Comments</h3>
                    <div class="comments-list">
        """
        
        for comment in request.comments:
            html += f"""
                        <div class="comment">
                            <strong>{comment.reviewer_name}</strong> - {comment.section}<br>
                            <em>{comment.comment_type}</em>: {comment.comment_text}<br>
                            <small>{comment.timestamp.strftime('%Y-%m-%d %H:%M')}</small>
                        </div>
            """
        
        html += """
                    </div>
                </div>
            </div>
            
            <script>
                function approve(requestId) {
                    // Collect all comments and checklist
                    const comment = document.getElementById('expert-comment').value;
                    if (comment) {
                        // Save comment before approving
                        fetch('/api/review/comment', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                request_id: requestId,
                                comment: comment,
                                section: document.getElementById('comment-section').value,
                                type: document.getElementById('comment-type').value
                            })
                        });
                    }
                    
                    // Approve the document
                    fetch('/api/review/approve', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({request_id: requestId})
                    }).then(() => {
                        alert('PDF approved and sent to customer!');
                        window.location.href = '/review/queue';
                    });
                }
                
                function requestChanges(requestId) {
                    const comment = document.getElementById('expert-comment').value;
                    if (!comment) {
                        alert('Please add a comment explaining the required changes');
                        return;
                    }
                    
                    fetch('/api/review/changes', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            request_id: requestId,
                            changes_requested: comment
                        })
                    }).then(() => {
                        alert('Changes requested. AI will regenerate the report.');
                        window.location.href = '/review/queue';
                    });
                }
                
                function scheduleCall(requestId) {
                    const reason = prompt('Why schedule a call? (e.g., "Complex findings need explanation")');
                    if (reason) {
                        fetch('/api/review/schedule-call', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                request_id: requestId,
                                reason: reason
                            })
                        }).then(() => {
                            alert('Call scheduling request sent to customer success team');
                        });
                    }
                }
            </script>
        </body>
        </html>
        """
        
        return html
    
    def approve_pdf(self, request_id: str, final_comments: Optional[str] = None) -> bool:
        """Approve PDF and prepare for delivery"""
        request = self.get_request(request_id)
        if not request:
            return False
        
        # Generate final PDF with comments incorporated
        final_pdf_path = f"{self.review_queue_path}/approved/{request.request_id}_final.pdf"
        
        # In production, would regenerate PDF with comments
        # For now, just update the path
        request.final_pdf_path = final_pdf_path
        request.status = ReviewStatus.APPROVED
        
        # Add to learning feedback
        self._capture_learning(request)
        
        self.save_review_queue()
        
        logger.info(f"Approved request {request_id}")
        return True
    
    def _capture_learning(self, request: PDFReviewRequest):
        """Capture learnings from human review for AI improvement"""
        learning_data = {
            "request_id": request.request_id,
            "framework": request.framework,
            "customer_type": self._classify_customer(request.customer_name),
            "comments": [
                {
                    "section": c.section,
                    "type": c.comment_type,
                    "text": c.comment_text
                }
                for c in request.comments
            ],
            "review_time": (datetime.now() - request.created_at).total_seconds() / 3600,
            "priority": request.priority
        }
        
        # Save to learning database
        learning_file = f"data/learning/reviews_{datetime.now().strftime('%Y%m')}.jsonl"
        os.makedirs("data/learning", exist_ok=True)
        
        with open(learning_file, 'a') as f:
            f.write(json.dumps(learning_data) + '\n')
    
    def _classify_customer(self, customer_name: str) -> str:
        """Classify customer type for learning patterns"""
        # Simple classification - in production would be more sophisticated
        if any(term in customer_name.lower() for term in ['bank', 'financial', 'capital']):
            return 'financial_services'
        elif any(term in customer_name.lower() for term in ['health', 'medical', 'pharma']):
            return 'healthcare'
        elif any(term in customer_name.lower() for term in ['tech', 'software', 'systems']):
            return 'technology'
        else:
            return 'general'
    
    def get_request(self, request_id: str) -> Optional[PDFReviewRequest]:
        """Get a specific review request"""
        for request in self.review_queue:
            if request.request_id == request_id:
                return request
        return None
    
    def get_pending_reviews(self, reviewer_id: Optional[str] = None) -> List[PDFReviewRequest]:
        """Get all pending review requests"""
        pending = [r for r in self.review_queue 
                  if r.status in [ReviewStatus.PENDING_REVIEW, ReviewStatus.IN_REVIEW]]
        
        if reviewer_id:
            pending = [r for r in pending 
                      if r.assigned_reviewer == reviewer_id or r.assigned_reviewer is None]
        
        # Sort by priority and due date
        priority_order = {'urgent': 0, 'high': 1, 'normal': 2, 'low': 3}
        pending.sort(key=lambda x: (priority_order.get(x.priority, 99), x.due_date))
        
        return pending
    
    def save_review_queue(self):
        """Persist review queue to disk"""
        queue_file = f"{self.review_queue_path}/review_queue.json"
        queue_data = []
        
        for request in self.review_queue:
            data = {
                "request_id": request.request_id,
                "draft_pdf_path": request.draft_pdf_path,
                "customer_name": request.customer_name,
                "framework": request.framework,
                "assessment_date": request.assessment_date.isoformat(),
                "created_at": request.created_at.isoformat(),
                "due_date": request.due_date.isoformat(),
                "status": request.status.value,
                "assigned_reviewer": request.assigned_reviewer,
                "priority": request.priority,
                "review_checklist": request.review_checklist,
                "comments": [
                    {
                        "comment_id": c.comment_id,
                        "reviewer_id": c.reviewer_id,
                        "reviewer_name": c.reviewer_name,
                        "timestamp": c.timestamp.isoformat(),
                        "section": c.section,
                        "comment_type": c.comment_type,
                        "comment_text": c.comment_text,
                        "resolution": c.resolution,
                        "resolved_at": c.resolved_at.isoformat() if c.resolved_at else None
                    }
                    for c in request.comments
                ],
                "version": request.version,
                "final_pdf_path": request.final_pdf_path,
                "delivered_at": request.delivered_at.isoformat() if request.delivered_at else None,
                "customer_feedback": request.customer_feedback
            }
            queue_data.append(data)
        
        with open(queue_file, 'w') as f:
            json.dump(queue_data, f, indent=2)
    
    def load_review_queue(self):
        """Load review queue from disk"""
        queue_file = f"{self.review_queue_path}/review_queue.json"
        if not os.path.exists(queue_file):
            return
        
        with open(queue_file, 'r') as f:
            queue_data = json.load(f)
        
        self.review_queue = []
        for data in queue_data:
            comments = []
            for c in data.get("comments", []):
                comment = ReviewComment(
                    comment_id=c["comment_id"],
                    reviewer_id=c["reviewer_id"],
                    reviewer_name=c["reviewer_name"],
                    timestamp=datetime.fromisoformat(c["timestamp"]),
                    section=c["section"],
                    comment_type=c["comment_type"],
                    comment_text=c["comment_text"],
                    resolution=c.get("resolution"),
                    resolved_at=datetime.fromisoformat(c["resolved_at"]) if c.get("resolved_at") else None
                )
                comments.append(comment)
            
            request = PDFReviewRequest(
                request_id=data["request_id"],
                draft_pdf_path=data["draft_pdf_path"],
                customer_name=data["customer_name"],
                framework=data["framework"],
                assessment_date=datetime.fromisoformat(data["assessment_date"]),
                created_at=datetime.fromisoformat(data["created_at"]),
                due_date=datetime.fromisoformat(data["due_date"]),
                status=ReviewStatus(data["status"]),
                assigned_reviewer=data.get("assigned_reviewer"),
                priority=data.get("priority", "normal"),
                review_checklist=data.get("review_checklist", self.standard_checklist),
                comments=comments,
                version=data.get("version", 1),
                final_pdf_path=data.get("final_pdf_path"),
                delivered_at=datetime.fromisoformat(data["delivered_at"]) if data.get("delivered_at") else None,
                customer_feedback=data.get("customer_feedback")
            )
            self.review_queue.append(request)
    
    def _notify_reviewers(self, request: PDFReviewRequest):
        """Notify reviewers of new request (placeholder for email/Slack)"""
        notification = f"""
        New PDF Review Request:
        Customer: {request.customer_name}
        Framework: {request.framework}
        Priority: {request.priority}
        Due: {request.due_date}
        
        Review at: /review/{request.request_id}
        """
        logger.info(f"Notification sent: {notification}")
    
    def get_review_metrics(self) -> Dict[str, Any]:
        """Get metrics on review process"""
        total_reviews = len(self.review_queue)
        pending = len([r for r in self.review_queue if r.status == ReviewStatus.PENDING_REVIEW])
        in_review = len([r for r in self.review_queue if r.status == ReviewStatus.IN_REVIEW])
        approved = len([r for r in self.review_queue if r.status == ReviewStatus.APPROVED])
        
        # Calculate average review time
        completed_reviews = [r for r in self.review_queue if r.status in [ReviewStatus.APPROVED, ReviewStatus.DELIVERED]]
        if completed_reviews:
            avg_review_time = sum(
                (r.delivered_at or datetime.now() - r.created_at).total_seconds() / 3600
                for r in completed_reviews
            ) / len(completed_reviews)
        else:
            avg_review_time = 0
        
        # Most common comment types
        all_comments = []
        for r in self.review_queue:
            all_comments.extend(r.comments)
        
        comment_types = {}
        for c in all_comments:
            comment_types[c.comment_type] = comment_types.get(c.comment_type, 0) + 1
        
        return {
            "total_reviews": total_reviews,
            "pending": pending,
            "in_review": in_review,
            "approved": approved,
            "avg_review_time_hours": round(avg_review_time, 2),
            "comment_distribution": comment_types,
            "total_comments": len(all_comments)
        }


# Example usage
if __name__ == "__main__":
    # Initialize workflow
    workflow = PDFReviewWorkflow()
    
    # Create a sample review request
    review_request = workflow.create_review_request(
        draft_pdf_path="reports/draft_SOC2_report.pdf",
        customer_name="Acme Corp",
        framework="SOC 2",
        assessment_data={"score": 94, "findings": 12},
        priority="high",
        due_in_hours=12
    )
    
    print(f"Created review request: {review_request.request_id}")
    
    # Assign reviewer
    workflow.assign_reviewer(review_request.request_id, "john.doe@sentinelgrc.com")
    
    # Add expert comment
    workflow.add_expert_comment(
        request_id=review_request.request_id,
        reviewer_id="john.doe@sentinelgrc.com",
        reviewer_name="John Doe",
        section="Executive Summary",
        comment_type="insight",
        comment_text="Consider mentioning the upcoming SOC 2 Type II audit timeline and preparation steps."
    )
    
    # Generate review interface
    html = workflow.generate_review_interface(review_request.request_id)
    
    # Get metrics
    metrics = workflow.get_review_metrics()
    print(f"Review metrics: {json.dumps(metrics, indent=2)}")