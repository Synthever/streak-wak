import requests
import re
from urllib.parse import urljoin, urlparse
import sys

class VulnerabilityScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.vulnerabilities = []

    def check_sql_injection(self):
        """Check for potential SQL injection vulnerabilities"""
        print("[+] Checking for SQL Injection vulnerabilities...")
        
        sql_payloads = ["'", "1' OR '1'='1", "'; DROP TABLE users; --"]
        
        try:
            for payload in sql_payloads:
                test_url = f"{self.target_url}?id={payload}"
                response = self.session.get(test_url, timeout=10)
                
                # Check for common SQL error messages
                sql_errors = [
                    "mysql_fetch_array()",
                    "ORA-01756",
                    "Microsoft OLE DB Provider for ODBC Drivers",
                    "PostgreSQL query failed",
                    "Warning: mysql_"
                ]
                
                for error in sql_errors:
                    if error.lower() in response.text.lower():
                        self.vulnerabilities.append(f"Potential SQL Injection found with payload: {payload}")
                        break
        except Exception as e:
            print(f"Error testing SQL injection: {e}")

    def check_xss(self):
        """Check for Cross-Site Scripting vulnerabilities"""
        print("[+] Checking for XSS vulnerabilities...")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
        
        try:
            for payload in xss_payloads:
                test_url = f"{self.target_url}?search={payload}"
                response = self.session.get(test_url, timeout=10)
                
                if payload in response.text:
                    self.vulnerabilities.append(f"Potential XSS vulnerability found with payload: {payload}")
        except Exception as e:
            print(f"Error testing XSS: {e}")

    def check_security_headers(self):
        """Check for missing security headers"""
        print("[+] Checking security headers...")
        
        try:
            response = self.session.get(self.target_url, timeout=10)
            headers = response.headers
            
            security_headers = {
                'X-Frame-Options': 'Missing X-Frame-Options header (Clickjacking protection)',
                'X-XSS-Protection': 'Missing X-XSS-Protection header',
                'X-Content-Type-Options': 'Missing X-Content-Type-Options header',
                'Strict-Transport-Security': 'Missing HSTS header',
                'Content-Security-Policy': 'Missing Content Security Policy header'
            }
            
            for header, message in security_headers.items():
                if header not in headers:
                    self.vulnerabilities.append(message)
                    
        except Exception as e:
            print(f"Error checking security headers: {e}")

    def check_directory_traversal(self):
        """Check for directory traversal vulnerabilities"""
        print("[+] Checking for Directory Traversal vulnerabilities...")
        
        traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd"
        ]
        
        try:
            for payload in traversal_payloads:
                test_url = f"{self.target_url}?file={payload}"
                response = self.session.get(test_url, timeout=10)
                
                # Check for common file contents
                if "root:" in response.text or "localhost" in response.text:
                    self.vulnerabilities.append(f"Potential Directory Traversal found with payload: {payload}")
                    
        except Exception as e:
            print(f"Error testing directory traversal: {e}")

    def check_open_redirect(self):
        """Check for open redirect vulnerabilities"""
        print("[+] Checking for Open Redirect vulnerabilities...")
        
        redirect_payloads = [
            "http://evil.com",
            "//evil.com",
            "https://google.com"
        ]
        
        try:
            for payload in redirect_payloads:
                test_url = f"{self.target_url}?redirect={payload}"
                response = self.session.get(test_url, timeout=10, allow_redirects=False)
                
                if response.status_code in [301, 302, 303, 307, 308]:
                    location = response.headers.get('Location', '')
                    if payload in location:
                        self.vulnerabilities.append(f"Potential Open Redirect found with payload: {payload}")
                        
        except Exception as e:
            print(f"Error testing open redirect: {e}")

    def scan(self):
        """Run all vulnerability checks"""
        print(f"[*] Starting vulnerability scan on: {self.target_url}")
        print("=" * 60)
        
        # Run all checks
        self.check_sql_injection()
        self.check_xss()
        self.check_security_headers()
        self.check_directory_traversal()
        self.check_open_redirect()
        
        # Display results
        print("\n" + "=" * 60)
        print("[*] Scan Results:")
        print("=" * 60)
        
        if self.vulnerabilities:
            print(f"[!] Found {len(self.vulnerabilities)} potential vulnerabilities:")
            for i, vuln in enumerate(self.vulnerabilities, 1):
                print(f"{i}. {vuln}")
        else:
            print("[+] No obvious vulnerabilities found in basic scan.")
        
        print("\n[!] Note: This is a basic scanner. For comprehensive testing, use professional tools.")

def main():
    print("Website Vulnerability Scanner")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("Enter target URL (e.g., http://example.com): ").strip()
    
    if not target_url:
        print("[-] Please provide a valid URL")
        return
    
    # Add protocol if missing
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    try:
        # Validate URL
        parsed_url = urlparse(target_url)
        if not parsed_url.netloc:
            print("[-] Invalid URL format")
            return
        
        # Create scanner and run scan
        scanner = VulnerabilityScanner(target_url)
        scanner.scan()
        
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
