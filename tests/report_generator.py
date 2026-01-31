"""Generate HTML test report from test execution logs."""
import json
from pathlib import Path
from datetime import datetime


def generate_html_report(test_results, output_file="reports/test_report.html"):
    """Generate a simple HTML report from test results.
    
    Args:
        test_results: List of dicts with test info
        output_file: Path to write HTML report
    """
    Path("reports").mkdir(exist_ok=True)
    
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Playwright API Test Report</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                border-bottom: 3px solid #007bff;
                padding-bottom: 10px;
            }
            .summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }
            .stat-card.passed {
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            }
            .stat-card.failed {
                background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
            }
            .stat-card.skipped {
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            }
            .stat-number {
                font-size: 32px;
                font-weight: bold;
                margin: 10px 0;
            }
            .stat-label {
                font-size: 14px;
                opacity: 0.9;
            }
            .test-section {
                margin: 30px 0;
            }
            .test-case {
                background: #f9f9f9;
                border-left: 4px solid #007bff;
                padding: 15px;
                margin: 10px 0;
                border-radius: 4px;
            }
            .test-case.passed {
                border-left-color: #28a745;
            }
            .test-case.failed {
                border-left-color: #dc3545;
            }
            .test-name {
                font-weight: bold;
                color: #333;
                margin-bottom: 5px;
            }
            .test-status {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                margin: 5px 0;
            }
            .test-status.passed {
                background: #d4edda;
                color: #155724;
            }
            .test-status.failed {
                background: #f8d7da;
                color: #721c24;
            }
            .test-details {
                background: white;
                padding: 10px;
                margin-top: 10px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                max-height: 300px;
                overflow-y: auto;
            }
            .request-response {
                margin: 10px 0;
                padding: 10px;
                background: #f0f0f0;
                border-radius: 4px;
            }
            .timestamp {
                color: #666;
                font-size: 12px;
            }
            footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #666;
                text-align: center;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧪 Playwright API Test Report</h1>
            <p class="timestamp">Generated: {timestamp}</p>
            
            <div class="summary">
                <div class="stat-card">
                    <div class="stat-label">Total Tests</div>
                    <div class="stat-number">{total}</div>
                </div>
                <div class="stat-card passed">
                    <div class="stat-label">Passed</div>
                    <div class="stat-number">{passed}</div>
                </div>
                <div class="stat-card failed">
                    <div class="stat-label">Failed</div>
                    <div class="stat-number">{failed}</div>
                </div>
                <div class="stat-card skipped">
                    <div class="stat-label">Skipped</div>
                    <div class="stat-number">{skipped}</div>
                </div>
            </div>
            
            <div class="test-section">
                <h2>Test Details</h2>
                {test_details}
            </div>
            
            <footer>
                <p>Playwright API Automation Framework</p>
                <p>Endpoint: /api/v1/intelligent-builder-intake/process</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    # Calculate stats
    passed = sum(1 for t in test_results if t.get("status") == "passed")
    failed = sum(1 for t in test_results if t.get("status") == "failed")
    skipped = sum(1 for t in test_results if t.get("status") == "skipped")
    total = len(test_results)
    
    # Build test details HTML
    test_details_html = ""
    for test in test_results:
        status_class = test.get("status", "unknown")
        test_details_html += f"""
        <div class="test-case {status_class}">
            <div class="test-name">{test.get('name', 'Unknown')}</div>
            <span class="test-status {status_class}">{test.get('status', 'UNKNOWN').upper()}</span>
            <div class="request-response">
                <strong>Request:</strong> {test.get('request', 'N/A')}
            </div>
            <div class="request-response">
                <strong>Response:</strong> {test.get('response', 'N/A')}
            </div>
            {f'<div class="test-details">{test.get("error", "")}</div>' if test.get("error") else ""}
        </div>
        """
    
    html = html.format(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total=total,
        passed=passed,
        failed=failed,
        skipped=skipped,
        test_details=test_details_html,
    )
    
    Path(output_file).write_text(html)
    print(f"✓ HTML report written to {output_file}")
