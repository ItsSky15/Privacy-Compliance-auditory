import requests
from bs4 import BeautifulSoup
import time

def analyze_site(url):
    try:
        print("🔍 Scanning the website... Please wait.")
        time.sleep(2)

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        score = calculate_privacy_score(soup, response)
        privacy_policy_exists = check_privacy_policy(soup)
        permissions = detect_permissions(soup)
        cookies = analyze_cookies(response)
        trackers = detect_trackers(soup)
        security_headers = check_security_headers(response.headers)
        compliance = check_compliance(soup)

        permissions_message, flagged_permissions = analyze_permission_overuse(permissions, url)
        dangerous_permissions = [perm for perm in permissions if perm in ['Camera/Microphone Access', 'Clipboard Access', 'Geolocation']]
        dangerous_message = (
            "⚠️ Dangerous permissions detected: " + ", ".join(dangerous_permissions)
            if dangerous_permissions
            else "✅ No dangerous permissions detected."
        )

        return {
            'score': score,
            'privacy_policy': {'exists': privacy_policy_exists},
            'permissions': permissions_message,
            'flagged_permissions': flagged_permissions,
            'dangerous_permissions': dangerous_message,
            'cookies': cookies,
            'trackers': trackers,
            'security_headers': security_headers,
            'compliance': compliance,
            'tips': generate_tips(dangerous_permissions, flagged_permissions, cookies)
        }
    except requests.exceptions.RequestException as e:
        return {'error': f"Error fetching the URL: {e}"}
    except Exception as e:
        return {'error': f"An unexpected error occurred: {e}"}


def calculate_privacy_score(soup, response):
    """
    Calculate a privacy score based on the presence of trackers, security headers, and privacy policy.
    """
    score = 100  # Start with a perfect score

    # Deduct points for missing privacy policy
    if not check_privacy_policy(soup):
        score -= 20

    # Deduct points for trackers
    trackers = detect_trackers(soup)
    score -= len(trackers) * 10  # Deduct 10 points per tracker

    # Deduct points for missing security headers
    headers = check_security_headers(response.headers)
    if len(headers) < 3:  # Assuming 3 critical headers
        score -= (3 - len(headers)) * 10

    # Deduct points for permissions requested
    permissions = detect_permissions(soup)
    if permissions:
        score -= len(permissions) * 5  # Deduct 5 points per permission

    # Ensure the score is within bounds
    return max(0, min(score, 100))


def check_privacy_policy(soup):
    """
    Check if a privacy policy link exists on the page.
    """
    privacy_links = soup.find_all('a', href=True, text=lambda t: 'privacy' in t.lower())
    return len(privacy_links) > 0


def detect_permissions(soup):
    """
    Detect if the website requests permissions like notifications, camera, microphone, geolocation, clipboard, etc.
    """
    permissions = []
    scripts = soup.find_all('script', src=True)

    # Check for specific APIs or keywords in scripts
    for script in scripts:
        if 'Notification' in script['src']:
            permissions.append('Notifications')
        if 'getUserMedia' in script['src'] or 'navigator.mediaDevices' in script['src']:
            permissions.append('Camera/Microphone Access')
        if 'geolocation' in script['src']:
            permissions.append('Geolocation')
        if 'clipboard' in script['src']:
            permissions.append('Clipboard Access')

    # Check inline scripts for permissions
    inline_scripts = soup.find_all('script')
    for script in inline_scripts:
        script_content = script.string or ""
        if 'Notification' in script_content:
            permissions.append('Notifications')
        if 'getUserMedia' in script_content or 'navigator.mediaDevices' in script_content:
            permissions.append('Camera/Microphone Access')
        if 'geolocation' in script_content:
            permissions.append('Geolocation')
        if 'clipboard' in script_content:
            permissions.append('Clipboard Access')

    return list(set(permissions))  # Remove duplicates


def analyze_permission_overuse(permissions, url):
    """
    Analyze if permissions requested are unnecessary based on the website's purpose.
    """
    flagged_permissions = []
    domain_keywords = {
        'shopping': ['Camera/Microphone Access', 'Geolocation'],
        'social': ['Clipboard Access', 'Camera/Microphone Access'],
        'news': ['Notifications', 'Geolocation']
    }

    # Example logic to flag unnecessary permissions
    for keyword, flagged in domain_keywords.items():
        if keyword in url:
            for permission in permissions:
                if permission in flagged:
                    flagged_permissions.append(permission)

    explanation = []
    for perm in flagged_permissions:
        if perm == 'Camera/Microphone Access':
            explanation.append("This website is asking for microphone access — which isn’t needed for its core purpose.")
        elif perm == 'Geolocation':
            explanation.append("This website is asking for your location — which isn’t necessary for its functionality.")
        elif perm == 'Clipboard Access':
            explanation.append("This website is accessing your clipboard — which could be a privacy risk.")
        elif perm == 'Notifications':
            explanation.append("This website is requesting notifications — which may not be essential.")

    return (
        "⚠️ Unnecessary permissions detected: " + ", ".join(flagged_permissions) if flagged_permissions else "✅ No unnecessary permissions detected.",
        explanation
    )


def analyze_cookies(response):
    """
    Analyze cookies to detect first-party, third-party, and fingerprinting attempts.
    """
    cookies = response.cookies.get_dict()
    cookie_analysis = {
        'first_party': [],
        'third_party': [],
        'fingerprinting': [],
        'explanations': []
    }

    for cookie_name, cookie_value in cookies.items():
        if 'facebook' in cookie_name or 'google' in cookie_name:
            cookie_analysis['third_party'].append(cookie_name)
            cookie_analysis['explanations'].append(f"🍪 {cookie_name}: Sends your activity to third-party services like Facebook or Google.")
        elif 'session' in cookie_name or 'auth' in cookie_name:
            cookie_analysis['first_party'].append(cookie_name)
            cookie_analysis['explanations'].append(f"🍪 {cookie_name}: Necessary for maintaining your session on the website.")
        elif 'fingerprint' in cookie_name or 'track' in cookie_name:
            cookie_analysis['fingerprinting'].append(cookie_name)
            cookie_analysis['explanations'].append(f"🕵️‍♂️ {cookie_name}: May be used for fingerprinting your device.")

    return cookie_analysis


def detect_trackers(soup):
    """
    Detect common tracking scripts (e.g., Google Analytics, Facebook Pixel).
    """
    trackers = []
    scripts = soup.find_all('script', src=True)
    for script in scripts:
        if 'google-analytics' in script['src'] or 'facebook' in script['src']:
            trackers.append(script['src'])
    return trackers


def check_security_headers(headers):
    """
    Check for the presence of common security headers.
    """
    required_headers = ['Content-Security-Policy', 'Strict-Transport-Security', 'X-Frame-Options']
    return [header for header in required_headers if header in headers]


def check_compliance(soup):
    """
    Check for compliance with GDPR and DPDP (India's Digital Personal Data Protection Act 2023).
    """
    # GDPR compliance check
    cookie_banner = soup.find(string=lambda text: 'cookie' in text.lower() and 'consent' in text.lower())
    gdpr_compliance = {
        'compliant': bool(cookie_banner),
        'missing': 'Cookie consent banner' if not cookie_banner else None
    }

    # DPDP compliance check
    privacy_notice = soup.find(string=lambda text: 'privacy notice' in text.lower() or 'data protection' in text.lower())
    consent_mechanism = soup.find(string=lambda text: 'consent' in text.lower() and 'manage' in text.lower())
    dpdp_compliance = {
        'compliant': bool(privacy_notice and consent_mechanism),
        'missing': []
    }
    if not privacy_notice:
        dpdp_compliance['missing'].append('Privacy notice')
    if not consent_mechanism:
        dpdp_compliance['missing'].append('Consent management mechanism')

    return {
        'GDPR': gdpr_compliance,
        'DPDP': dpdp_compliance
    }


def generate_tips(dangerous_permissions, flagged_permissions, cookies):
    """
    Generate tips for users to protect their data based on detected permissions and cookies.
    """
    tips = [
        "✅ Always verify the website's authenticity before sharing personal data.",
        "✅ Avoid sharing sensitive information like OTPs or passwords.",
        "✅ Use browser extensions to block trackers and ads.",
        "✅ Regularly clear your browser cookies and cache."
    ]

    if 'Camera/Microphone Access' in dangerous_permissions:
        tips.append("⚠️ Avoid granting camera or microphone access unless absolutely necessary.")
    if 'Geolocation' in dangerous_permissions:
        tips.append("⚠️ Be cautious about sharing your location with websites.")
    if 'Clipboard Access' in dangerous_permissions:
        tips.append("⚠️ Avoid copying sensitive information while browsing this site.")

    if flagged_permissions:
        tips.append("⚠️ Review the permissions requested by this website and deny unnecessary ones.")

    if cookies['third_party']:
        tips.append("⚠️ This website uses third-party cookies. Consider blocking them for better privacy.")
    if cookies['fingerprinting']:
        tips.append("⚠️ Fingerprinting attempts detected. Use anti-fingerprinting browser extensions.")

    return tips


# Example usage
if __name__ == "__main__":
    url = input("Enter the URL to analyze: ").strip()
    result = analyze_site(url)
    print(result)