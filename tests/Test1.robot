*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${URL}            http://localhost:8501
${BROWSER}        chrome

*** Test Cases ***
Test Example
    Log To Console    test1
    Open Browser    ${URL}    ${BROWSER}
#    Wait Until Page Contains Element    v3    timeout=5s FIXME not seing app
#    Wait Until Page Contains Element    App    timeout=2
    Page Should Contain  Demo
    Sleep    2
#    Click Element    //*[contains(text(),'v2') or contains(text(),'v1')]
#    Sleep    1
#    Page Should Contain    You didn't select comedy
    Close Browser
