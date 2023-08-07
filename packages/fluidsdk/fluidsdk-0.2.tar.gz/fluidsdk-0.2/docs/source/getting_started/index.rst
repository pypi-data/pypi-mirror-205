Getting started
===========================

WorkHack bots are trained using the blueprint of a conversation, we call these blueprints a flow.
A flow is a dictionary that has the steps of a conversation and fluid is the language created by WorkHack to build a flow. 
The fluidsdk has all the methods to help you build a bot capable of having human-like conversations utilizing the capabilities of Large Language Models.

Installation
------------------

FluidSDK can be installing using pip by issuing the following command.

>>> pip install fluidsdk

After you have installed the sdk, you can check if it is installing by
opening a python shell and importing `fluidsdk`.

>>> import fluidsdk

Hello World!
------------------

We start by creating a flow Object.

.. code-block:: python

    from fluidsdk.pyrite import FlowBuilder
   
    flow = FlowBuilder("Flow Id", "Flow Name", token="SUPER_SECRET_ACCESS_TOKEN")

The fluidsdk library has wide range of intents that help the bot understand the conversation expectations. 
One of the most basic intents is :py:mod:`fluidsdk.pyrite.library.say`, all it does is send the user a message. 

.. code-block:: python

    from fluidsdk.pyrite.library import say
   
    @flow.subroutine   #The decorator ``@FLOW_OBJECT.subroutine`` registers a subroutine.
    def start():
        say("Hello World!")
       
    flow.build()    #Builds the registered subroutine.
   
``flow.build()`` builds the conversation flow dictionary. 
This can either either be stored in a dict object to be used later, or passed onto our conversation_engine which processess the steps in the flow and trains a bot for the desired conversation.

Adding another subroutine.
------------------------------

There is another intent called :py:mod:`fluidsdk.pyrite.library.ask` which asks a question and stores the answer which can be used through the rest of the conversation. 
This is what the final code would look like with two subroutines:

.. code-block:: python

    from fluidsdk.pyrite import FlowBuilder
    from fluidsdk.pyrite.library import say, ask
    
    flow = FlowBuilder("Flow Id", "Flow Name", token="SUPER_SECRET_ACCESS_TOKEN")
    
    @flow.subroutine
    def check_did_homework():
        homework = ask("Did you do your homework?")
        
    @flow.subroutine  
    def start():
        say("Hello World!")
        check_did_homework()
       
    flow.build()


What's Next?
--------------------
You can find functionality of other intents and methods you can use to build more complex conversations.
Go through ``example.py`` to understand how you can build on top of the simple bot created here. 

.. literalinclude:: example.py