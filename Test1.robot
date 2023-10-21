*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${URL}            https://decenter-ai.streamlit.app/
${BROWSER}        chrome

*** Test Cases ***
Test Example
    Log To Console    test1
    Open Browser    ${URL}    ${BROWSER}
    Wait Until Page Contains Element    v3    timeout=20s
    Page Should Contain    You selected v3.
    Sleep    2
    Click Element    //*[contains(text(),'v2') or contains(text(),'v1')]
    Sleep    1
    Page Should Contain    You didn't select comedy
    Close Browser