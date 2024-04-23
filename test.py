"""
Test Cases :

Logic check :

    Positive check :
    If the user is smiling, ensure that the smile is being detected and stored in the right place, in the computer it is running on.

    Negative check :
    If the user is not smiling the application is not expected to do anything except staying in idle state.

Boundary check :
In extreme cases, in some environments smiles may not be detected.
Test the system under low-light conditions or harsh lighting conditions that might affect the accuracy of smile detection. The system should still provide appropriate feedback or capture a selfie if a smile is detected.
Test the application with extreme cases, such as very subtle smiles or exaggerated smiles, to see if it still accurately detects and captures selfies.

Concurrency Test Case:
Check if the application can handle multiple users smiling simultaneously and capture selfies accordingly.

Insufficient Resources:
Stress test the system by running it on a device with limited resources. It should not crash or freeze but instead degrade gracefully.

Error Handling :
If the memory is becoming full the user should be warned about it and if the memory is full the application is not crashing and gracefully tells to user the that it could not work anymore.


"""