Updated 11/11/2016

Files and their purpose:

----------CardEngine\Engine.py----------
Variables available:
None

Functions available:
None

Classes available:
EventHandler: Used to call a list of functions.  Essentially used to send events to interested parties
StandardPlayingCard: Defines a suit, value, and player for a standard playing card
CardUI: UI associated with a particular card
CardEngine: Engine used to process user events and handle UI Elements

----------CardEngine\Hitbox.py----------
Variables available:
None

Functions available:
None

Classes Available:
SquareHitbox: hitbox for UI Elements that can be rotated as needed.  Rotation based around center (currently topleft)
Point: Used to define a particular 2d point in space
Vector: Used to define a vector between two 2d points in space

----------CardEngine\UI.py----------
Variables available:
-UI_Font: font used to display text on screen
-Colors: Commonly used colors, listed as follows
    -BLACK
    -DARKGRAY
    -GRAY
    -LIGHTGRAY
    -LIGHTGRAY2
    -WHITE
    -TRANSPARENT
    -GREEN

Functions available:
-init(): Used to initialize setting up the fonts

Classes available:
-UIElement: Generic UI Element that allows the programmer to define unique UI Elements.
-Text: Displays text to screen
-Textbox: Allows user to enter text and uses callback upon pressing enter
-Button: Button that can be clicked that uses a callback upon being pressed
-Checkbox: Allows user to check/uncheck a box and uses a callback upon changing checked state
-PyText: See Text.  Allows programmer to override several functions
-PyTextbox: See Textbox.  Allows programmer to override several functions.  No callback function
-PyButton: See Button.  Allows programmer to override several functions.  No callback function
-PyCheckbox: See Checkbox.  Allows programmer to override several functions.  No callback function

----------Core\AI\AI.py----------
Variables available:
None

Functions available:
None

Classes available:
HumanAI: AI used for players
ComputerAI: AI used for computer to act as a player

----------Core\CardLogging.py----------
Variables available:
log_file: Implements logger class

Functions available:
None

Classes available:
Logger: Used to create log file and allow programmer to log stuff

----------Core\Constant.py----------
Variables available:
None

Functions available:
None

Classes available:
Suit: acts as enum for suit
Value: acts as enum for value
Suit_str: actually a list, but is the string representation of the string enum
Value_str: actually a list, but is the string representation of the value enum
Check: acts as enum for Decision Tree to check between trick pile and player's hand
Comparison Type: act as enum for Decision Tree to determine comparison check

----------Core\Heart.py----------
Variables available:
None

Functions available:
None

Classes available:
Player: Holds information about the player and includes the AI
Hearts: Class to setup initial conditions to the game and updates the engine

----------Core\Screen.py----------
Variables available:
None

Functions available:
None

Classes available:
None

----------StateMachine\State.py----------
Variables available:
None

Functions available:
None

Classes available:
State: Base state that defines functions that State Machine will use
Setup State: Sets up the deck and the hands of each player, as well setting up variables to default values
Passing State: State for passing cards between players
Playing State: State to determine playing order, and figure out who gets card in a round
Scoring State: State to determine scores based on the tricks each player has

----------StateMachine\StateMachine.py----------
Variables available:
None

Functions available:
None

Classes available:
State Machine: Interacts with States and allows states to transition

----------Setup.py----------
Used to create an executable

----------Play.py----------
Used as entry point to play Hearts