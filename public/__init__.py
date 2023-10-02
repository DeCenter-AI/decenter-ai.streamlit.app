from utils.inputs.css import extract_css
from utils.inputs.html import extract_html

public_dir = "static/"

index_css = extract_css(f"public/index.css")

# index_css = """
# <link href="./static/index.css" rel="stylesheet">
# """

logo = "static/logo.png"

report_request_buttons_html = extract_html(
    f"public/report-request-feature-buttons.html",
)

button_styles_css = """
<style>
.report-button, .request-button {
    padding: 5px 10px;
    border-radius: 3px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 10px;
    text-decoration: none;
    transition: background-color 0.3s, color 0.3s; /* Add smooth transitions for background color and text color */
}

.report-button {
    background-color: #e84242;
    color: #000 !important;
}

.report-button:hover {
    color: #000 !important; /* Change text color on hover to black */
    text-decoration: none;
}

.request-button {
    background-color: #FFFF00;
    color: #000 !important;

}

.request-button:hover {
    color: #000 !important; /* Change text color on hover to black */
    text-decoration: none;
}

.button-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: absolute;
    top: 230px;
    left: 50px;
}

/* Style for default-text and hover-text */
.request-button .hover-text, .report-button .hover-text {
    display: none; /* Hide hover-text by default */
}

.request-button:hover .hover-text, .report-button:hover .hover-text {
    display: inline; /* Show hover-text on hover */
}

.request-button .default-text, .report-button .default-text {
    display: inline; /* Show default-text initially */
}

.request-button:hover .default-text, .report-button:hover .default-text {
    display: none; /* Hide default-text on hover */
}
</style>
"""
