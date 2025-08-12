"""
ML Integration for Sentinel GRC - Lightweight Implementation
============================================================
Adds machine learning capabilities to enhance confidence scoring and anomaly detection
without requiring extensive ML infrastructure.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sentence_transformers import SentenceTransformer
import joblib
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class MLPrediction:
    """Structure for ML prediction results"""
    prediction: float
    confidence: float
    explanation: str
    model_features: Dict[str, float]
    anomaly_score: Optional[float] = None

class ComplianceMLEngine:
    """
    Lightweight ML engine for compliance assessments.
    Focuses on practical enhancements rather than complex models.
    """
    
    def __init__(self, models_dir="./models"):
        self.models_dir = models_dir
        self.confidence_model = None
        self.anomaly_detector = None
        self.scaler = StandardScaler()
        
        # Use lightweight sentence transformer for document analysis
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize with synthetic data if models don't exist
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models with synthetic training data"""
        
        logger.info("Initializing ML models...")
        
        try:
            # Try to load existing models
            self.confidence_model = joblib.load(f"{self.models_dir}/confidence_model.pkl")
            self.anomaly_detector = joblib.load(f"{self.models_dir}/anomaly_model.pkl")
            self.scaler = joblib.load(f"{self.models_dir}/scaler.pkl")
            logger.info("Loaded existing ML models")
            
        except FileNotFoundError:
            # Create models with synthetic data
            logger.info("Creating new ML models with synthetic data")
            self._train_synthetic_models()
    
    def _train_synthetic_models(self):
        """Train models using synthetic compliance data"""
        
        # Generate synthetic training data based on realistic compliance patterns
        synthetic_data = self._generate_synthetic_training_data()
        
        # Prepare features and targets
        X = synthetic_data['features']
        y_confidence = synthetic_data['confidence_scores']
        
        # Train confidence model
        self.confidence_model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        self.confidence_model.fit(X_scaled, y_confidence)
        
        # Train anomaly detector
        self.anomaly_detector = IsolationForest(
            contamination=0.1,  # Expect 10% anomalies
            random_state=42
        )
        self.anomaly_detector.fit(X_scaled)
        
        # Save models
        import os
        os.makedirs(self.models_dir, exist_ok=True)
        
        joblib.dump(self.confidence_model, f"{self.models_dir}/confidence_model.pkl")
        joblib.dump(self.anomaly_detector, f"{self.models_dir}/anomaly_model.pkl")
        joblib.dump(self.scaler, f"{self.models_dir}/scaler.pkl")
        
        logger.info("Trained and saved ML models")
    
    def _generate_synthetic_training_data(self) -> Dict[str, np.ndarray]:
        """Generate realistic synthetic training data"""
        
        n_samples = 1000
        
        # Features: [controls_implemented, gaps_found, company_size, industry_risk, 
        #           previous_incidents, has_policies, complexity_score]
        
        np.random.seed(42)
        
        features = []
        confidence_scores = []
        
        for _ in range(n_samples):
            # Simulate company characteristics
            controls_implemented = np.random.randint(0, 9)  # 0-8 Essential 8 controls
            gaps_found = 8 - controls_implemented + np.random.randint(-1, 3)
            gaps_found = max(0, min(gaps_found, 8))
            
            company_size = np.random.choice([0, 1, 2, 3], p=[0.4, 0.3, 0.2, 0.1])  # SMB to enterprise
            industry_risk = np.random.uniform(0, 1)
            previous_incidents = np.random.choice([0, 1], p=[0.7, 0.3])
            has_policies = np.random.choice([0, 1], p=[0.4, 0.6])
            complexity_score = np.random.uniform(0, 1)
            
            # Calculate realistic confidence score based on features
            base_confidence = 0.5
            
            # Controls boost confidence
            base_confidence += (controls_implemented / 8) * 0.3
            
            # Gaps reduce confidence
            base_confidence -= (gaps_found / 8) * 0.25
            
            # Company size affects confidence (larger = more complex = lower confidence)
            base_confidence -= company_size * 0.05
            
            # High-risk industries reduce confidence
            if industry_risk > 0.7:
                base_confidence -= 0.1
            
            # Previous incidents reduce confidence
            if previous_incidents:
                base_confidence -= 0.1
            
            # Policies increase confidence
            if has_policies:
                base_confidence += 0.1
            
            # Add some noise
            base_confidence += np.random.normal(0, 0.05)
            
            # Ensure confidence is between 0 and 1
            confidence = max(0.1, min(0.95, base_confidence))
            
            # Convert to categorical for classification (Low, Medium, High confidence)
            if confidence >= 0.8:
                confidence_category = 2  # High
            elif confidence >= 0.6:
                confidence_category = 1  # Medium
            else:
                confidence_category = 0  # Low
            
            features.append([
                controls_implemented, gaps_found, company_size, industry_risk,
                previous_incidents, has_policies, complexity_score
            ])
            confidence_scores.append(confidence_category)
        
        return {
            'features': np.array(features),
            'confidence_scores': np.array(confidence_scores)
        }
    
    def enhance_agent_confidence(self, assessment_data: Dict[str, Any]) -> MLPrediction:
        """
        Use ML to enhance confidence scoring from rule-based agents.
        """
        
        try:
            # Extract features from assessment
            features = self._extract_assessment_features(assessment_data)
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Get ML confidence prediction
            ml_confidence_class = self.confidence_model.predict(features_scaled)[0]
            ml_confidence_proba = self.confidence_model.predict_proba(features_scaled)[0]
            
            # Convert class to confidence score
            confidence_mapping = {0: 0.5, 1: 0.7, 2: 0.9}
            ml_confidence = confidence_mapping[ml_confidence_class]
            
            # Get feature importance for explanation
            feature_names = [
                "controls_implemented", "gaps_found", "company_size", "industry_risk",
                "previous_incidents", "has_policies", "complexity_score"
            ]
            
            feature_importance = dict(zip(feature_names, features))
            
            # Detect anomalies
            anomaly_score = self.anomaly_detector.decision_function(features_scaled)[0]
            is_anomaly = self.anomaly_detector.predict(features_scaled)[0] == -1
            
            # Generate explanation
            explanation = self._generate_confidence_explanation(
                ml_confidence_class, feature_importance, is_anomaly
            )
            
            return MLPrediction(
                prediction=ml_confidence,
                confidence=float(max(ml_confidence_proba)),
                explanation=explanation,
                model_features=feature_importance,
                anomaly_score=float(anomaly_score)
            )
            
        except Exception as e:
            logger.error(f"Error in ML confidence enhancement: {e}")
            
            # Fallback to conservative prediction
            return MLPrediction(
                prediction=0.6,
                confidence=0.5,
                explanation="ML prediction unavailable, using conservative estimate",
                model_features={}
            )
    
    def _extract_assessment_features(self, assessment_data: Dict[str, Any]) -> List[float]:
        """Extract ML features from assessment data"""
        
        # Safe feature extraction with defaults
        controls_implemented = len(assessment_data.get('controls_assessed', []))
        gaps_found = len(assessment_data.get('gaps_identified', []))
        
        # Company size (0=small, 1=medium, 2=large, 3=enterprise)
        company_size = 0
        if 'company_profile' in assessment_data:
            employee_count = assessment_data['company_profile'].employee_count
            if employee_count > 1000:
                company_size = 3
            elif employee_count > 200:
                company_size = 2
            elif employee_count > 50:
                company_size = 1
        
        # Industry risk (simplified mapping)
        industry_risk = 0.5  # Default medium risk
        if 'company_profile' in assessment_data:
            high_risk_industries = ['Healthcare', 'Finance', 'Government', 'Defense']
            if assessment_data['company_profile'].industry in high_risk_industries:
                industry_risk = 0.8
        
        # Previous incidents
        previous_incidents = 0
        if 'company_profile' in assessment_data:
            if assessment_data['company_profile'].previous_incidents:
                previous_incidents = 1
        
        # Has policies (based on current controls)
        has_policies = 0
        if 'company_profile' in assessment_data:
            controls = assessment_data['company_profile'].current_controls or []
            policy_indicators = ['Policies', 'Procedures', 'Training', 'Governance']
            if any(indicator in ' '.join(controls) for indicator in policy_indicators):
                has_policies = 1
        
        # Complexity score (based on number of frameworks and requirements)
        complexity_score = min(1.0, (controls_implemented + gaps_found) / 16)
        
        return [
            controls_implemented, gaps_found, company_size, industry_risk,
            previous_incidents, has_policies, complexity_score
        ]
    
    def _generate_confidence_explanation(self, confidence_class: int, 
                                       features: Dict[str, float], 
                                       is_anomaly: bool) -> str:
        """Generate human-readable explanation for confidence prediction"""
        
        explanations = []
        
        # Confidence level explanation
        if confidence_class == 2:
            explanations.append("High confidence due to comprehensive control implementation")
        elif confidence_class == 1:
            explanations.append("Medium confidence with adequate but improvable controls")
        else:
            explanations.append("Low confidence due to significant compliance gaps")
        
        # Key contributing factors
        controls = int(features.get('controls_implemented', 0))
        gaps = int(features.get('gaps_found', 0))
        
        if controls >= 6:
            explanations.append(f"Strong control implementation ({controls}/8)")
        elif controls >= 4:
            explanations.append(f"Moderate control implementation ({controls}/8)")
        else:
            explanations.append(f"Limited control implementation ({controls}/8)")
        
        if gaps <= 2:
            explanations.append("Few compliance gaps identified")
        elif gaps <= 4:
            explanations.append("Several compliance gaps need attention")
        else:
            explanations.append("Many compliance gaps require urgent attention")
        
        # Anomaly detection
        if is_anomaly:
            explanations.append("⚠️ Unusual pattern detected - manual review recommended")
        
        return ". ".join(explanations) + "."
    
    def analyze_document_compliance(self, documents: List[str]) -> Dict[str, Any]:
        """
        Use NLP to analyze documents for compliance-relevant content.
        """
        
        if not documents:
            return {"relevant_sections": [], "compliance_indicators": {}}
        
        try:
            # Generate embeddings for documents
            doc_embeddings = self.embedder.encode(documents)
            
            # Define compliance-related queries
            compliance_queries = {
                "privacy_policy": "privacy policy personal data protection",
                "security_controls": "security controls cybersecurity information security",
                "incident_response": "incident response cyber incident security breach",
                "access_control": "access control user authentication authorization",
                "data_governance": "data governance data management data retention",
                "risk_management": "risk assessment risk management security risk",
                "training": "security training awareness training cyber training",
                "monitoring": "security monitoring threat monitoring vulnerability"
            }
            
            # Generate query embeddings
            query_embeddings = {}
            for category, query in compliance_queries.items():
                query_embeddings[category] = self.embedder.encode([query])[0]
            
            # Find relevant sections
            relevant_sections = []
            compliance_indicators = {}
            
            for doc_idx, doc_embedding in enumerate(doc_embeddings):
                doc_relevance = {}
                
                for category, query_embedding in query_embeddings.items():
                    # Calculate similarity
                    similarity = np.dot(doc_embedding, query_embedding) / (
                        np.linalg.norm(doc_embedding) * np.linalg.norm(query_embedding)
                    )
                    doc_relevance[category] = float(similarity)
                
                # Check if document is relevant (threshold = 0.3)
                max_similarity = max(doc_relevance.values())
                if max_similarity > 0.3:
                    best_category = max(doc_relevance, key=doc_relevance.get)
                    relevant_sections.append({
                        "document_index": doc_idx,
                        "relevance_category": best_category,
                        "similarity_score": max_similarity,
                        "document_preview": documents[doc_idx][:200] + "..."
                    })
                
                # Update compliance indicators
                for category, score in doc_relevance.items():
                    if category not in compliance_indicators:
                        compliance_indicators[category] = []
                    compliance_indicators[category].append(score)
            
            # Summarize compliance indicators
            for category in compliance_indicators:
                scores = compliance_indicators[category]
                compliance_indicators[category] = {
                    "max_relevance": float(max(scores)),
                    "avg_relevance": float(np.mean(scores)),
                    "documents_found": sum(1 for s in scores if s > 0.3)
                }
            
            return {
                "relevant_sections": relevant_sections[:10],  # Top 10 most relevant
                "compliance_indicators": compliance_indicators,
                "total_documents_analyzed": len(documents),
                "total_relevant_documents": len(relevant_sections)
            }
            
        except Exception as e:
            logger.error(f"Error in document analysis: {e}")
            return {"relevant_sections": [], "compliance_indicators": {}, "error": str(e)}
    
    def detect_compliance_anomalies(self, company_profile, assessment_results: List[Dict]) -> Dict[str, Any]:
        """
        Detect unusual patterns in compliance assessments that might indicate 
        data quality issues or special circumstances requiring human review.
        """
        
        if len(assessment_results) < 2:
            return {"anomalies_detected": False, "reason": "Insufficient data for anomaly detection"}
        
        try:
            # Extract features from all assessments
            features_matrix = []
            
            for assessment in assessment_results:
                features = self._extract_assessment_features(assessment)
                features_matrix.append(features)
            
            # Scale features
            features_scaled = self.scaler.transform(features_matrix)
            
            # Detect anomalies
            anomaly_predictions = self.anomaly_detector.predict(features_scaled)
            anomaly_scores = self.anomaly_detector.decision_function(features_scaled)
            
            # Identify anomalies
            anomalies = []
            for i, (prediction, score) in enumerate(zip(anomaly_predictions, anomaly_scores)):
                if prediction == -1:  # Anomaly detected
                    anomalies.append({
                        "assessment_index": i,
                        "framework": assessment_results[i].get("framework", "Unknown"),
                        "anomaly_score": float(score),
                        "severity": "HIGH" if score < -0.5 else "MEDIUM"
                    })
            
            # Generate anomaly report
            if anomalies:
                return {
                    "anomalies_detected": True,
                    "anomaly_count": len(anomalies),
                    "anomalies": anomalies,
                    "recommendations": [
                        "Manual review recommended for flagged assessments",
                        "Verify assessment input data accuracy",
                        "Consider industry-specific factors",
                        "Check for data collection errors"
                    ]
                }
            else:
                return {
                    "anomalies_detected": False,
                    "assessments_analyzed": len(assessment_results),
                    "confidence": "Normal patterns detected"
                }
                
        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
            return {"anomalies_detected": False, "error": str(e)}
    
    def update_model_with_feedback(self, assessment_features: List[float], 
                                 actual_confidence: float, feedback_score: float):
        """
        Update model with human feedback (for continuous learning).
        In production, this would retrain models periodically.
        """
        
        # For now, just log the feedback
        logger.info(f"Feedback received - Features: {assessment_features}, "
                   f"Actual confidence: {actual_confidence}, "
                   f"Feedback score: {feedback_score}")
        
        # In production, you would:
        # 1. Store feedback in database
        # 2. Periodically retrain models
        # 3. A/B test model improvements
        # 4. Monitor model drift
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded ML models"""
        
        return {
            "confidence_model": {
                "type": "RandomForestClassifier",
                "features": ["controls_implemented", "gaps_found", "company_size", 
                           "industry_risk", "previous_incidents", "has_policies", "complexity_score"],
                "classes": ["Low Confidence", "Medium Confidence", "High Confidence"]
            },
            "anomaly_detector": {
                "type": "IsolationForest",
                "contamination_rate": 0.1
            },
            "document_analyzer": {
                "type": "SentenceTransformer",
                "model": "all-MiniLM-L6-v2",
                "capabilities": ["semantic_search", "compliance_categorization"]
            }
        }


# Integration example with existing agents
def integrate_ml_with_existing_agent(existing_assessment: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example of how to integrate ML enhancements with your existing agent assessments.
    """
    
    # Initialize ML engine
    ml_engine = ComplianceMLEngine()
    
    # Get ML-enhanced confidence
    ml_prediction = ml_engine.enhance_agent_confidence(existing_assessment)
    
    # Combine rule-based and ML confidence
    rule_confidence = existing_assessment.get('confidence', 0.7)
    final_confidence = 0.6 * ml_prediction.prediction + 0.4 * rule_confidence
    
    # Add ML insights to assessment
    enhanced_assessment = existing_assessment.copy()
    enhanced_assessment.update({
        'ml_enhanced': True,
        'ml_confidence': ml_prediction.prediction,
        'ml_explanation': ml_prediction.explanation,
        'combined_confidence': final_confidence,
        'anomaly_score': ml_prediction.anomaly_score,
        'requires_review': ml_prediction.anomaly_score and ml_prediction.anomaly_score < -0.3
    })
    
    return enhanced_assessment


# Example usage
if __name__ == "__main__":
    # Initialize ML engine
    ml_engine = ComplianceMLEngine()
    
    # Test with synthetic assessment data
    test_assessment = {
        'framework': 'Essential8',
        'controls_assessed': [{'control': f'E8_{i}'} for i in range(1, 6)],  # 5 controls
        'gaps_identified': [{'control': f'E8_{i}'} for i in range(6, 9)],    # 3 gaps
        'confidence': 0.7,
        'company_profile': type('obj', (object,), {
            'employee_count': 150,
            'industry': 'Healthcare',
            'previous_incidents': ['Phishing 2023'],
            'current_controls': ['MFA', 'Backups', 'Policies']
        })
    }
    
    # Test ML enhancement
    ml_result = ml_engine.enhance_agent_confidence(test_assessment)
    print(f"ML Confidence: {ml_result.prediction:.2f}")
    print(f"ML Explanation: {ml_result.explanation}")
    print(f"Anomaly Score: {ml_result.anomaly_score:.3f}")
    
    # Test document analysis
    sample_documents = [
        "Our privacy policy outlines how we protect personal data and comply with regulations",
        "Security controls include multi-factor authentication and regular backups",
        "Incident response procedures are documented and tested quarterly"
    ]
    
    doc_analysis = ml_engine.analyze_document_compliance(sample_documents)
    print(f"\nDocument Analysis - Relevant sections found: {len(doc_analysis['relevant_sections'])}")
    
    # Display model information
    model_info = ml_engine.get_model_info()
    print(f"\nLoaded models: {list(model_info.keys())}")