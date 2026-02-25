"""
Email Notification Tool
Sends email notifications when:
- A new employer message arrives
- A final response is approved and sent
- An unknown question is detected (human intervention needed)
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
import logging

logger = logging.getLogger(__name__)


def send_email_notification(
    subject: str,
    body: str,
    notification_type: str = "info"
) -> bool:
    """
    Send an email notification via Gmail SMTP.
    
    Args:
        subject: Email subject
        body: Email body (HTML supported)
        notification_type: Type of notification (new_message, response_sent, unknown_question)
    
    Returns:
        True if sent successfully, False otherwise
    """
    if not settings.EMAIL_SENDER or not settings.EMAIL_PASSWORD:
        logger.warning("Email credentials not configured. Skipping notification.")
        return False
    
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = settings.EMAIL_SENDER
        msg["To"] = settings.EMAIL_RECEIVER
        msg["Subject"] = f"[Career Agent] {subject}"
        
        # Color coding based on notification type
        color_map = {
            "new_message": "#3498db",      # Blue
            "response_sent": "#2ecc71",     # Green
            "unknown_question": "#e74c3c",  # Red
            "info": "#95a5a6"               # Gray
        }
        color = color_map.get(notification_type, "#95a5a6")
        
        html_body = f"""
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: {color}; color: white; padding: 15px 20px; border-radius: 8px 8px 0 0;">
                <h2 style="margin: 0;">🤖 Career Assistant Agent</h2>
                <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 14px;">{notification_type.replace('_', ' ').title()}</p>
            </div>
            <div style="background: #f8f9fa; padding: 20px; border: 1px solid #dee2e6; border-top: none; border-radius: 0 0 8px 8px;">
                {body}
            </div>
            <p style="color: #95a5a6; font-size: 12px; text-align: center; margin-top: 10px;">
                Sent by Career Assistant AI Agent
            </p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, "html"))
        
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email notification sent: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")
        return False


def notify_new_message(sender_name: str, message_preview: str) -> bool:
    """Notify about a new employer message."""
    body = f"""
    <h3>📩 New Message from Employer</h3>
    <p><strong>From:</strong> {sender_name}</p>
    <div style="background: white; padding: 15px; border-left: 4px solid #3498db; margin: 10px 0; border-radius: 4px;">
        <p style="margin: 0; color: #333;">{message_preview}</p>
    </div>
    <p style="color: #666;">The Career Agent is generating a response...</p>
    """
    return send_email_notification(
        subject=f"New Message from {sender_name}",
        body=body,
        notification_type="new_message"
    )


def notify_response_sent(sender_name: str, response_preview: str, score: float) -> bool:
    """Notify that a response has been approved and sent."""
    body = f"""
    <h3>✅ Response Approved & Sent</h3>
    <p><strong>To:</strong> {sender_name}</p>
    <p><strong>Evaluation Score:</strong> {score}/10</p>
    <div style="background: white; padding: 15px; border-left: 4px solid #2ecc71; margin: 10px 0; border-radius: 4px;">
        <p style="margin: 0; color: #333;">{response_preview[:500]}...</p>
    </div>
    """
    return send_email_notification(
        subject=f"Response Sent to {sender_name} (Score: {score}/10)",
        body=body,
        notification_type="response_sent"
    )


def notify_unknown_question(sender_name: str, message: str, category: str, confidence: float) -> bool:
    """Notify that an unknown question was detected - human intervention needed."""
    body = f"""
    <h3>⚠️ Human Intervention Required</h3>
    <p><strong>From:</strong> {sender_name}</p>
    <p><strong>Category:</strong> <span style="color: #e74c3c; font-weight: bold;">{category.replace('_', ' ').title()}</span></p>
    <p><strong>Confidence Score:</strong> {confidence}</p>
    <div style="background: white; padding: 15px; border-left: 4px solid #e74c3c; margin: 10px 0; border-radius: 4px;">
        <p style="margin: 0; color: #333;">{message}</p>
    </div>
    <p style="color: #e74c3c; font-weight: bold;">
        🔔 The agent has low confidence in handling this message. Please review and respond manually.
    </p>
    """
    return send_email_notification(
        subject=f"⚠️ Unknown Question from {sender_name} - Action Required",
        body=body,
        notification_type="unknown_question"
    )


def send_response_to_employer(
    employer_email: str,
    employer_name: str,
    response_text: str
) -> bool:
    """Send the AI-generated response directly to the employer's email."""
    if not settings.EMAIL_SENDER or not settings.EMAIL_PASSWORD:
        logger.warning("Email credentials not configured. Cannot send to employer.")
        return False
    
    if not employer_email or not employer_email.strip():
        logger.warning("No employer email provided. Skipping.")
        return False
    
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = settings.EMAIL_SENDER
        msg["To"] = employer_email.strip()
        msg["Subject"] = f"Re: Your message - Burak Yalçın"
        
        html_body = f"""
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #2c3e50; color: white; padding: 15px 20px; border-radius: 8px 8px 0 0;">
                <h2 style="margin: 0;">Burak Yalçın</h2>
                <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 14px;">Career Assistant</p>
            </div>
            <div style="background: #f8f9fa; padding: 20px; border: 1px solid #dee2e6; border-top: none; border-radius: 0 0 8px 8px;">
                <p style="white-space: pre-wrap; color: #333; line-height: 1.6;">{response_text}</p>
            </div>
            <p style="color: #95a5a6; font-size: 11px; text-align: center; margin-top: 10px;">
                This response was generated by Burak Yalçın's Career Assistant AI Agent
            </p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, "html"))
        
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Response sent to employer: {employer_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send response to employer: {e}")
        return False

