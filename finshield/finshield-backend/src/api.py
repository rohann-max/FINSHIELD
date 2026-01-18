import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Initialize database
def init_db():
    conn = sqlite3.connect('security.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id TEXT PRIMARY KEY,
                  timestamp TEXT,
                  amount REAL,
                  merchant TEXT,
                  risk_score INTEGER,
                  decision TEXT,
                  reason TEXT)''')
    conn.commit()
    conn.close()

init_db()

class FraudDetectionEngine:
    def analyze(self, data):
        factors = []
        risk_score = 0
        is_bot = False

        # Extract parameters
        wpm = data.get('typingWPM', 0)
        interval = data.get('keystrokeInterval', 0)
        variance = data.get('keystrokeVariance', 0)
        backspaces = data.get('backspaceCount', 0)
        amount = data.get('amount', 0)
        merchant = data.get('merchantType', 'retail')
        wps = data.get('typingWPS', 0)
        cps = data.get('typingCPS', 0)
        click_delay = data.get('clickDelay', 0)
        click_interval = data.get('clickInterval', 0)
        double_tap_rate = data.get('doubleTapRate', 0)
        scroll_speed = data.get('scrollSpeed', 0)
        scroll_distance = data.get('scrollDistance', 0)
        scroll_changes = data.get('scrollDirectionChanges', 0)
        scroll_events = data.get('scrollEventCount', 0)
        field_focus = data.get('fieldFocusTimeSec', 0)
        tab_switches = data.get('tabSwitches', 0)
        device_type = data.get('deviceType', 'desktop')
        screen_width = data.get('screenWidth', 0)
        screen_height = data.get('screenHeight', 0)
        interaction_density = data.get('interactionDensity', 0)
        total_dwell = data.get('totalDwellTime', 0)
        mouse_speed = data.get('mouseSpeed', 0)
        time_away = data.get('timeAwayFromTab', 0)
        orientation_events = data.get('deviceOrientationEvents', 0)
        is_webdriver = data.get('isWebDriver', False)
        is_debugger_open = data.get('isDebuggerOpen', False)
        plugins_length = data.get('pluginsLength', 0)

        # 1. Typing Speed (WPM)
        if wpm > 300 or wpm < 20:
            is_bot = True
            risk_score += 80
            status = "critical"
            reason = f"Impossible typing speed ({wpm} WPM)"
        else:
            status = "normal"
            reason = "Normal typing speed"
        
        factors.append({"id": "wpm", "name": "Typing Speed", "value": f"{wpm} WPM", "status": status, "reason": reason})

        # 1.5. Words Per Second
        wps = wpm / 60
        if wps > 5 or wps < 0.33:
            risk_score += 25
            status = "critical"
            reason = f"Impossible WPS ({wps:.1f})"
        else:
            status = "normal"
            reason = "Normal WPS"
        
        factors.append({"id": "wps", "name": "Words Per Second", "value": f"{wps:.1f} WPS", "status": status, "reason": reason})

        # 2. Keystroke Timing
        if 0 < interval < 30:
            is_bot = True
            risk_score += 50
            status = "critical"
            reason = "Impossible keystroke intervals (<30ms)"
        elif 0 < interval < 60:
            risk_score += 30
            status = "critical"
            reason = "Very fast intervals (30-60ms)"
        elif interval < 100:
            risk_score += 10
            status = "warning"
            reason = "Fast intervals (60-100ms)"
        else:
            status = "normal"
            reason = "Normal human intervals"
        
        factors.append({"id": "interval", "name": "Keystroke Timing", "value": f"{interval}ms", "status": status, "reason": reason})

        # 3. Rhythmic Consistency
        if 0 < variance < 5 and wpm > 50:
            is_bot = True
            risk_score += 45
            status = "critical"
            reason = "Perfect mechanical consistency"
        elif 0 < variance < 15 and wpm > 40:
            risk_score += 25
            status = "critical"
            reason = "Highly consistent timing"
        elif variance < 30:
            risk_score += 5
            status = "warning"
            reason = "Consistent typing pattern"
        else:
            status = "normal"
            reason = "Natural human variance"
        
        factors.append({"id": "variance", "name": "Rhythmic Variance", "value": f"{variance}ms", "status": status, "reason": reason})

        # 4. Mouse Speed
        if mouse_speed > 8000:
            is_bot = True
            risk_score += 40
            status = "critical"
            reason = "Impossible mouse speed (>8000 px/ms)"
        elif mouse_speed > 5000:
            risk_score += 25
            status = "critical"
            reason = "Extremely fast mouse (>5000 px/ms)"
        elif mouse_speed > 3000:
            risk_score += 15
            status = "warning"
            reason = "Very fast mouse (3000-5000 px/ms)"
        elif mouse_speed > 1500:
            risk_score += 5
            status = "warning"
            reason = "Fast mouse movement"
        else:
            status = "normal"
            reason = "Normal mouse speed"
        
        factors.append({"id": "mouse", "name": "Mouse Speed", "value": f"{mouse_speed} px/ms", "status": status, "reason": reason})

        # 5. Click Patterns
        if click_interval > 0 and click_interval < 50:
            risk_score += 30
            status = "critical"
            reason = "Automated clicking (<50ms intervals)"
        elif click_interval > 0 and click_interval < 100:
            risk_score += 15
            status = "warning"
            reason = "Very fast clicking (50-100ms)"
        elif click_interval > 0 and click_interval < 200:
            risk_score += 5
            status = "warning"
            reason = "Fast clicking (100-200ms)"
        else:
            status = "normal"
            reason = "Normal clicking pattern"
        
        factors.append({"id": "click", "name": "Click Timing", "value": f"{click_interval}ms", "status": status, "reason": reason})

        # 6. Scroll Behavior
        if scroll_speed > 2000:
            risk_score += 25
            status = "critical"
            reason = "Extremely fast scrolling (>2000 units/ms)"
        elif scroll_speed > 1000:
            risk_score += 15
            status = "warning"
            reason = "Very fast scrolling (1000-2000 units/ms)"
        elif scroll_speed > 500:
            risk_score += 5
            status = "warning"
            reason = "Fast scrolling (500-1000 units/ms)"
        else:
            status = "normal"
            reason = "Normal scrolling"
        
        factors.append({"id": "scroll", "name": "Scroll Speed", "value": f"{scroll_speed} units/ms", "status": status, "reason": reason})

        # 7. Interaction Density
        if interaction_density > 20:
            risk_score += 30
            status = "critical"
            reason = "Extremely high interaction density (>20/sec)"
        elif interaction_density > 10:
            risk_score += 15
            status = "warning"
            reason = "High interaction density (10-20/sec)"
        elif interaction_density > 5:
            risk_score += 5
            status = "warning"
            reason = "Moderate interaction density"
        elif interaction_density < 0.5:
            risk_score += 10
            status = "warning"
            reason = "Very low engagement"
        else:
            status = "normal"
            reason = "Normal interaction level"
        
        factors.append({"id": "density", "name": "Interaction Density", "value": f"{interaction_density:.1f} events/sec", "status": status, "reason": reason})

        # 8. Tab Switching
        if tab_switches > 15:
            risk_score += 25
            status = "critical"
            reason = "Excessive tab switching (>15)"
        elif tab_switches > 10:
            risk_score += 15
            status = "warning"
            reason = "Frequent tab switching (10-15)"
        elif tab_switches > 5:
            risk_score += 5
            status = "warning"
            reason = "Some tab switching"
        else:
            status = "normal"
            reason = "Normal tab usage"
        
        factors.append({"id": "tabs", "name": "Tab Activity", "value": f"{tab_switches} switches", "status": status, "reason": reason})

        # 9. Device Orientation Changes
        if orientation_events > 20:
            risk_score += 20
            status = "warning"
            reason = "Frequent device orientation changes"
        elif orientation_events > 10:
            risk_score += 10
            status = "warning"
            reason = "Some orientation changes"
        else:
            status = "normal"
            reason = "Stable device position"
        
        factors.append({"id": "orient", "name": "Device Stability", "value": f"{orientation_events} events", "status": status, "reason": reason})

        # 10. Field Focus Time
        if field_focus > 0 and field_focus < 2:
            risk_score += 15
            status = "warning"
            reason = "Very brief field focus (<2 sec)"
        elif field_focus > 0 and field_focus < 5:
            risk_score += 5
            status = "warning"
            reason = "Short field focus (2-5 sec)"
        else:
            status = "normal"
            reason = "Normal field engagement"
        
        factors.append({"id": "focus", "name": "Field Focus Time", "value": f"{field_focus} sec", "status": status, "reason": reason})

        # 11. Time Away from Tab
        if time_away > 300:
            risk_score += 20
            status = "warning"
            reason = "Long time away from tab (>5 min)"
        elif time_away > 120:
            risk_score += 10
            status = "warning"
            reason = "Extended time away (2-5 min)"
        elif time_away > 30:
            risk_score += 5
            status = "warning"
            reason = "Some time away (30 sec-2 min)"
        else:
            status = "normal"
            reason = "Active session"
        
        factors.append({"id": "away", "name": "Time Away", "value": f"{time_away} sec", "status": status, "reason": reason})

        # 12. Scroll Events Count
        if scroll_events > 100:
            risk_score += 15
            status = "warning"
            reason = "Excessive scrolling (>100 events)"
        elif scroll_events > 50:
            risk_score += 8
            status = "warning"
            reason = "Heavy scrolling (50-100 events)"
        elif scroll_events > 20:
            risk_score += 3
            status = "warning"
            reason = "Moderate scrolling"
        else:
            status = "normal"
            reason = "Normal scrolling activity"
        
        factors.append({"id": "scroll_count", "name": "Scroll Activity", "value": f"{scroll_events} events", "status": status, "reason": reason})

        # 13. Double Tap Rate
        if double_tap_rate > 20:
            risk_score += 20
            status = "critical"
            reason = "High double-tap rate (>20)"
        elif double_tap_rate > 10:
            risk_score += 10
            status = "warning"
            reason = "Moderate double-tap rate (10-20)"
        elif double_tap_rate > 5:
            risk_score += 5
            status = "warning"
            reason = "Some double-taps"
        else:
            status = "normal"
            reason = "Normal tapping"
        
        factors.append({"id": "double_tap", "name": "Double Tap Rate", "value": f"{double_tap_rate}", "status": status, "reason": reason})

        # 14. Backspace Count
        if backspaces > 10:
            risk_score += 15
            status = "warning"
            reason = "High correction rate (>10 backspaces)"
        elif backspaces > 5:
            risk_score += 8
            status = "warning"
            reason = "Moderate corrections (5-10)"
        elif backspaces > 2:
            risk_score += 3
            status = "warning"
            reason = "Some corrections"
        else:
            status = "normal"
            reason = "Few corrections"
        
        factors.append({"id": "backspace", "name": "Correction Rate", "value": f"{backspaces} backspaces", "status": status, "reason": reason})

        # 15. Merchant Risk
        m_risks = {'cryptocurrency': 40, 'jewelry': 30, 'gambling': 35, 'electronics': 20, 'travel': 15}
        m_score = m_risks.get(merchant, 0)
        if m_score > 0:
            risk_score += m_score
            status = "warning"
            reason = f"High-risk merchant category (+{m_score} risk)"
        else:
            status = "normal"
            reason = "Low-risk merchant"
        
        factors.append({"id": "merchant", "name": "Merchant Risk", "value": merchant.upper(), "status": status, "reason": reason})

        # 16. Environmental Integrity (Tampering Detection)
        tampering_indicators = []
        if is_webdriver:
            tampering_indicators.append("WebDriver detected")
        if is_debugger_open:
            tampering_indicators.append("Debugger open")
        if plugins_length == 0:
            tampering_indicators.append("No plugins")

        if tampering_indicators:
            risk_score += 40
            is_bot = True
            status = "critical"
            reason = f"Browser tampering detected: {', '.join(tampering_indicators)}"
        else:
            status = "normal"
            reason = "Clean browser environment"

        factors.append({"id": "environment", "name": "Environmental Integrity", "value": f"WebDriver:{is_webdriver}, Debugger:{is_debugger_open}, Plugins:{plugins_length}", "status": status, "reason": reason})
        
        # Determine final decision based on risk score
        decision = "BLOCKED" if risk_score >= 80 else "APPROVED"
        
        return {"decision": decision, "riskScore": min(100, risk_score), "factors": factors, "isBot": is_bot}

def get_azure_ai_text_analytics(factors, decision, risk_score):
    """Uses Azure OpenAI Text Analytics to generate the final forensic verdict"""
    try:
        # For now, return fallback response since Azure credentials are not configured
        if not os.getenv('AZURE_OPENAI_API_KEY') or os.getenv('AZURE_OPENAI_API_KEY') == 'your_azure_openai_api_key':
            # Analyze factors to generate intelligent verdict
            critical_factors = [f for f in factors if f['status'] == 'critical']
            warning_factors = [f for f in factors if f['status'] == 'warning']

            if decision == "BLOCKED" or risk_score >= 80:
                verdict = "Fraudulent Pattern"
                if critical_factors:
                    description = f"Multiple automation signatures detected: {', '.join([f['name'] for f in critical_factors[:3]])}. Risk score: {risk_score}%."
                else:
                    description = f"High-risk behavioral patterns identified. Risk score: {risk_score}%. Rule-based analysis suggests automated activity."
            elif warning_factors and risk_score >= 40:
                verdict = "Suspicious Activity"
                description = f"Concerning behavioral indicators: {', '.join([f['name'] for f in warning_factors[:2]])}. Risk score: {risk_score}%. Manual review recommended."
            else:
                verdict = "Authorized Human"
                normal_factors = [f for f in factors if f['status'] == 'normal']
                if normal_factors:
                    description = f"Natural human behavioral patterns observed: {', '.join([f['name'] for f in normal_factors[:2]])}. Risk score: {risk_score}%."
                else:
                    description = f"Behavioral analysis completed. Risk score: {risk_score}%. No suspicious patterns detected."

            return verdict, description

        # If credentials are configured, use Azure OpenAI
        from openai import AzureOpenAI

        client = AzureOpenAI(
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            api_version="2023-05-15",
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
        )

        # Create detailed factor summary for AI analysis
        factor_summary = "\n".join([f"- {f['name']}: {f['value']} ({f['status']}) - {f['reason']}" for f in factors])

        prompt = f"""
        Analyze the following comprehensive behavioral biometric data for fraud detection:

        RISK SCORE: {risk_score}%
        ENGINE DECISION: {decision}

        DETAILED FACTOR ANALYSIS:
        {factor_summary}

        Provide a professional forensic analysis in 2-3 sentences.
        Focus on the most suspicious behavioral patterns.
        If fraudulent, explain the automation signatures.
        If legitimate, highlight natural human characteristics.
        """

        response = client.chat.completions.create(
            model=os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4'),
            messages=[
                {"role": "system", "content": "You are an expert Azure AI Fraud Analyst specializing in behavioral biometrics. Provide detailed, professional forensic analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )

        description = response.choices[0].message.content.strip()

        # Determine verdict based on AI analysis and risk score
        if risk_score >= 80 or decision == "BLOCKED":
            verdict = "Fraudulent Pattern"
        elif risk_score >= 40:
            verdict = "Suspicious Activity"
        else:
            verdict = "Authorized Human"

        return verdict, description

    except Exception as e:
        print(f"Azure AI Connection Error: {e}")
        # Enhanced fallback with factor analysis
        critical_count = len([f for f in factors if f['status'] == 'critical'])
        warning_count = len([f for f in factors if f['status'] == 'warning'])

        if decision == "BLOCKED" or risk_score >= 80:
            verdict = "Fraudulent Pattern"
            description = f"Analysis failed but {critical_count} critical and {warning_count} warning factors suggest fraud. Risk: {risk_score}%."
        else:
            verdict = "Pattern Analysis"
            description = f"AI analysis unavailable. {critical_count} critical, {warning_count} warning factors. Risk: {risk_score}%. Manual review needed."

        return verdict, description

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    engine = FraudDetectionEngine()
    result = engine.analyze(data)
    
    # Call Azure AI Text Analytics
    verdict, desc = get_azure_ai_text_analytics(result['factors'], result['decision'], result['riskScore'])
    
    # Create single log entry dictionary
    log_entry = {
        'id': data.get('transactionId', 'unknown'),
        'timestamp': datetime.now().isoformat(),
        'amount': data.get('amount', 0),
        'merchant': data.get('merchantType', 'unknown'),
        'risk_score': result['riskScore'],
        'decision': result['decision'],
        'reason': f"{verdict}: {desc}"
    }
    
    # Single database insert with INSERT OR IGNORE
    conn = sqlite3.connect('security.db')
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO logs (id, timestamp, amount, merchant, risk_score, decision, reason)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (log_entry['id'], log_entry['timestamp'], log_entry['amount'], 
               log_entry['merchant'], log_entry['risk_score'], log_entry['decision'], log_entry['reason']))
    conn.commit()
    conn.close()
    
    return jsonify({
        **result,
        "aiVerdict": verdict,
        "aiDescription": desc,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('security.db')
    c = conn.cursor()
    c.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT 10')
    rows = c.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    history = []
    for row in rows:
        history.append({
            'id': row[0],
            'timestamp': row[1],
            'amount': row[2],
            'merchant': row[3],
            'risk_score': row[4],
            'decision': row[5],
            'reason': row[6]
        })
    
    return jsonify(history)

if __name__ == '__main__':
    app.run(port=3000, debug=True)