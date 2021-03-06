.. _fixtures:

Test Fixtures
=============

Slash includes a powerful mechanism for parametrizing and composing tests, called *fixtures*. This feature resembles, and was greatly inspired by, the feature of the same name in **py.test**.

To demonstrate this feature we will use *test functions*, but it also applies to test methods just the same.

What is a Fixture?
------------------

A *fixture* refers to a certain piece of setup or data that your test requires in order to run. It generally does not refer to the test itself, but the base on which the test builds to carry out its work.

Slash represents fixtures in the form of arguments to your test function, thus denoting that your test function needs this fixture in order to run:

.. code-block:: python

		def test_microwave_turns_on(microwave):
		    microwave.turn_on()
		    assert microwave.get_state() == STATE_ON

So far so good, but what exactly is *microwave*? Where does it come from? 

The answer is that Slash is responsible of looking up needed fixtures for each test being run. Each function is examined, and telling by its arguments, Slash goes ahead and looks for a fixture definition called *microwave*.

The Fixture Definition
----------------------

The fixture definition is where the logic of your fixture goes. Let's write the following somewhere in your file:

.. code-block:: python

		import slash

		...

		@slash.fixture
		def microwave():
		    # initialization of the actual microwave instance   
		    return Microwave(...)  


In addition to the test file itself, you can also put your fixtures in a file called `slashconf.py`, and put it in your test directory. Multiple such files can exist, and a test automatically "inherits" fixtures from the entire directory hierarchy above it.

Fixture Cleanups
----------------

You can control what happens when the lifetime of your fixture ends. By default, this happens at the end of each test that requested your fixture. To do this, add an argument for your fixture called `this`, and call its `add_cleanup` method with your cleanup callback:

.. code-block:: python

		@slash.fixture
		def microwave(this):
		    returned = Microwave()
		    this.add_cleanup(returned.turn_off)
		    return returned

Opting Out of Fixtures
----------------------

In some cases you may want to turn off Slash's automatic deduction of parameters as fixtures. For instance in the following case you want to explicitly call a version of a base class's ``before`` method:

.. code-block:: python
       
       >>> class BaseTest(slash.Test):
       ...     def before(self, param):
       ...         self._construct_case_with(param)

       >>> class DerivedTest(BaseTest):
       ...     @slash.parametrize('x', [1, 2, 3])
       ...     def before(self, x):
       ...         param_value = self._compute_param(x)
       ...         super(DerivedTest, self).before(x)

This case would fail to load, since Slash will assume ``param`` is a fixture name and will not find such a fixture to use. The solution is to use :func:`slash.nofixtures` on the parent class's ``before`` method to mark that ``param`` is *not* a fixture name:

.. code-block:: python
       
       >>> class BaseTest(slash.Test):
       ...     @slash.nofixtures
       ...     def before(self, param):
       ...         self._construct_case_with(param)



Fixture Needing Other Fixtures
------------------------------

A fixture can depend on other fixtures just like a test depends on the fixture itself, for instance, here is a fixture for a heating plate, which depends on the type of microwave we're testing:

.. code-block:: python

		@slash.fixture
		def heating_plate(microwave):
		    return get_appropriate_heating_plate_for(microwave)

Slash takes care of spanning the fixture dependency graph and filling in the values in the proper order. If a certain fixture is needed in multiple places in a single test execution, it is guaranteed to return the same value:

.. code-block:: python

		def test_heating_plate_usage(microwave, heating_plate):
		    # we can be sure that heating_plate matches the microwave,
		    # since `microwave` will return the same value for the test
		    # and for the fixture


Fixture Parametrization
-----------------------

Fixtures become interesting when you parametrize them. This enables composing many variants of tests with a very little amount of effort. Let's say we have many kinds of microwaves, we can easily parametrize the microwave class:


.. code-block:: python

		@slash.fixture
		@slash.parametrize('microwave_class', [SimpleMicrowave, AdvancedMicrowave]):
		def microwave(microwave_class, this):
		    returned = microwave_class()
		    this.add_cleanup(returned.turn_off)
		    return returned

Now that we have a parametrized fixture, Slash takes care of multiplying the test cases that rely on it automatically. The single test we wrote in the beginning will now cause two actual test cases to be loaded and run -- one with a simple microwave and one with an advanced microwave.

As you add more parametrizations into dependent fixtures in the dependency graph, the actual number of cases being run eventually multiples in a cartesian manner.

Fixture Scopes
--------------

By default, a fixture "lives" through only a single test at a time. This means that:

1. The fixture function will be called again for each new test needing the fixture
2. If any cleanups exist, they will be called at the end of each test needing the fixture.

We say that fixtures, by default, have a **scope of a single test**, or *test scope*.

Slash also supports *session* and *module* scoped fixtures. *Session fixtures* live from the moment of their activation until the end of the test session, while *module fixtures* live until the last test of the module that needed them finished execution. Specifying the scope is rather straightforward:

.. code-block:: python

		@slash.fixture(scope='session')
		def some_session_fixture(this):
		    @this.add_cleanup
		    def cleanup():
		        print('Hurray! the session has ended')
		

		@slash.fixture(scope='module')
		def some_module_fixture(this):
		    @this.add_cleanup
		    def cleanup():
		        print('Hurray! We are finished with this module')
		    

Autouse Fixtures
----------------

You can also "force" a fixture to be used, even if it is not required by any function argument. For instance, this example creates a temporary directory that is deleted at the end of the session:

.. code-block:: python

		@slash.fixture(autouse=True, scope='session')
		def temp_dir():
		    directory = '/some/directory'
		    os.makedirs(directory)

		    @this.add_cleanup
		    def cleanup():
		        shutil.rmtree(directory)
		    

