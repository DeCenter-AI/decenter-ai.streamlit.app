*** Settings ***
Library           SeleniumLibrary
Library           Process

*** Variables ***
${URL}            http://localhost:8501
${URL1}           http://localhost:8501/v1
${BROWSER}        chrome

*** Test Cases ***

Test Head
    Log To Console    test_head
    Open Browser    ${URL}    ${BROWSER}
    Sleep    5
    Go To    ${URL1}
    Sleep    5
    Page Should Contain  AI Infrastructure for Model training

    Page Should Contain Button  Train
    Click Button    Train
    Sleep           5
    Click Button    Train
#    Sleep           10
#    Page Should Contain Button    Download trained model
#    Click Button    Download trained model



    Sleep    5

    Close Browser