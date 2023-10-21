*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${URL}            http://localhost:8501
${BROWSER}        chrome

*** Test Cases ***
Test Head
    Log To Console    test_head
    Open Browser    ${URL}    ${BROWSER}
#    Wait Until Page Contains Element    v3    timeout=5s FIXME not seing app
#    Wait Until Page Contains Element    App    timeout=2
    Page Should Contain  Demo
    Sleep    2
    Page Should Contain  v3
    Page Should Contain  AI Infrastructure for Model training

#    Wait Until Page Contains Element  Train //FIXME

#    Click Element    //*[contains(text(),'v2') or contains(text(),'v1')]
#    Sleep    1
#    Page Should Contain    You didn't select comedy
    Close Browser
