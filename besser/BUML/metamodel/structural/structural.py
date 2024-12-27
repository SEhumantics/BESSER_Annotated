import time
from abc import ABC
from datetime import datetime, timedelta
from typing import Any, Dict, List, Set, Union, Optional

# Constant - Represents the unlimited value for the maximum multiplicity (capped at 9999).
UNLIMITED_MAX_MULTIPLICITY: int = int(9999)


class Element(ABC):
    """The `Element` class is the superclass of all structural elements in the B-UML metamodel.

    This class inherits from the `ABC` class.

    Notes
    -----
    This class is an abstract class and should not be instantiated.
    """

    pass


class NamedElement(Element):
    """The `NamedElement` class is the superclass of all structural elements with a name.

    This class inherits from the `Element` class.

    Attributes
    ----------
    name : str
        The name of the named element.

    timestamp : datetime
        The object creation datetime. By default it is set to the actual object creation time.
        See the `__init__` method for more details.

    synonyms : Optional[List[str]]
        The list of synonyms of the named element. By default it is `None`.

    visibility : str
        Determines the kind of visibility of the named element. By default it is `public`.

    Parameters
    ----------
    name : str
        The name of the named element.

    timestamp : Optional[datetime]
        The object creation datetime.

    synonyms : Optional[List[str]]
        The list of synonyms of the named element.

    visibility : str, optional
        Determines the kind of visibility of the named element.
    """

    def __init__(
        self,
        name: str,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
        visibility: str = "public",
    ):
        """Initialize an instace of the `NamedElement` class.

        See the class docstring for more details on `Parameters` and `Attributes`.
        """
        # Set the name of the named element.
        self.name: str = name

        # Set the timestamp of the named element.
        # If the timestamp is not provided, it is set to the time when the object is created.
        self.timestamp: datetime = (
            timestamp
            if timestamp is not None
            else datetime.now()
            + timedelta(microseconds=(time.perf_counter_ns() % 1_000_000) / 1000)
        )

        # Set the list of synonyms of the named element.
        self.synonyms: Optional[List[str]] = synonyms

        # Set the visibility of the named element.
        self.visibility: str = visibility

    @property
    def name(self) -> str:
        """Get the name of the named element.

        Returns
        -------
        name : str
            The name of the named element.
        """
        # Return the name of the named element.
        return self.__name

    @name.setter
    def name(self, name: str):
        """Set the name of the named element.

        Parameters
        ----------
        name : str
            The name of the named element.
        """
        # Set the name of the named element.
        self.__name = name

    @property
    def timestamp(self) -> datetime:
        """Get the timestamp of the named element.

        Returns
        -------
        timestamp : datetime
            The object creation datetime.
        """
        # Return the timestamp of the named element.
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        """Set the timestamp of the named element.

        Parameters
        ----------
        timestamp : datetime
            The object creation datetime.
        """
        # Set the timestamp of the named element.
        self.__timestamp = timestamp

    @property
    def synonyms(self) -> Optional[List[str]]:
        """Get the list of synonyms of the named element.

        Returns
        -------
        synonyms : Optional[List[str]]
            The list of synonyms of the named element.
        """
        # Return the list of synonyms of the named element.
        return self.__synonyms

    @synonyms.setter
    def synonyms(self, synonyms: List[str]):
        """Set the list of synonyms of the named element.

        Parameters
        ----------
        synonyms : List[str]
            The list of synonyms of the named element.
        """
        # Set the list of synonyms of the named element.
        self.__synonyms = synonyms

    @property
    def visibility(self) -> str:
        """Get the visibility of the named element.

        Returns
        -------
        visibility : str
            The visibility of the named element.
        """
        # Return the visibility of the named element.
        return self.__visibility

    @visibility.setter
    def visibility(self, visibility: str):
        """Set the visibility of the named element.

        Parameters
        ----------
        visibility : str
            The visibility of the named element.

        Raises
        ------
        ValueError
            If the visibility provided is none of these: `public`, `private`, `protected`, or `package`.
        """
        # Check if the provided visibility is valid.
        if visibility not in ["public", "private", "protected", "package"]:
            raise ValueError("Invalid value of visibility.")

        # Set the visibility of the named element.
        self.__visibility = visibility


class Type(NamedElement):
    """The `Type` class is the superclass of classes and data types in the B-UML metamodel.

    This class inherits from the `NamedElement` class.

    Attributes
    ----------
    name : str
        The name of the type. Inherits from `NamedElement`.

    timestamp : datetime
        The object creation datetime. Inherits from `NamedElement`.
        By default it is set to the actual object creation time.
        See the `__init__` method for more details.

    synonyms : Optional[List[str]]
        The list of synonyms of the type. Inherits from `NamedElement`.
        By default it is `None`.

    Parameters
    ----------
    name : str
        The name of the type.

    timestamp : Optional[datetime]
        The object creation datetime.

    synonyms : Optional[List[str]]
        The list of synonyms of the type.
    """

    def __init__(
        self,
        name: str,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        """Initialize an instance of the `Type` class.

        See the class docstring for more details on `Parameters` and `Attributes`.
        """
        # Initialize the `NamedElement` superclass.
        super().__init__(name, timestamp, synonyms)

    def __repr__(self) -> str:
        """Return a string representation of the `Type` object.

        The string representation includes the `name`, `timestamp`, and `synonyms` of the `Type` object.

        Returns
        -------
        str
            A string representation of the `Type` object.
        """
        # Return the string representation of the `Type` object.
        return f"Type({self.name}, {self.timestamp}, {self.synonyms})"


class DataType(Type):
    """The `DataType` class represents a data type in the B-UML metamodel.

    This class inherits from the `Type` class.
    """

    def __repr__(self) -> str:
        """Return a string representation of the `DataType` object.

        The string representation includes the `name` of the `DataType` object.

        Returns
        -------
        str
            A string representation of the `DataType` object.
        """
        # Return the string representation of the `DataType` object.
        return f"DataType({self.name})"


class PrimitiveDataType(DataType):
    """The `PrimitiveDataType` class represents a primitive data type with a specified name in the B-UML metamodel.

    This class inherits from the `DataType` class.
    """

    @NamedElement.name.setter  # type: ignore
    # Mypy does not recognize the setter decorator. See more: https://github.com/python/mypy/issues/5936.
    def name(self, name: str):
        """Set the name of the `PrimitiveDataType`.

        Parameters
        ----------
        name : str
            The name of the `PrimitiveDataType`.

        Raises
        ------
        ValueError
            If an invalid primitive data type is provided.
            Allowed values are `int`, `float`, `str`, `bool`, `time`, `date`,
            `datetime`, and `timedelta`.
        """

        # Check if the provided name is a valid primitive data type.
        if name not in [
            "int",
            "float",
            "str",
            "bool",
            "time",
            "date",
            "datetime",
            "timedelta",
        ]:
            raise ValueError("Invalid primitive data type.")

        # Set the name of the `PrimitiveDataType`.
        super(PrimitiveDataType, PrimitiveDataType).name.fset(self, name)

    def __repr__(self) -> str:
        """Return a string representation of the `PrimitiveDataType` object.

        The string representation includes the `name`, `timestamp`, and `synonyms` of the `PrimitiveDataType` object.

        Returns
        -------
        str
            A string representation of the `PrimitiveDataType` object.
        """
        # Return the string representation of the `PrimitiveDataType` object.
        return f"PrimitiveDataType({self.name}, {self.timestamp}, {self.synonyms})"


# Define a set of primitive data types.
# TODO: Should this encapsulation using walrus operator (:=) be kept? It should function the same way as the original solution, but it puts those PrimitiveDataType instances into the context of the primitive_data_types set (and is also available in the global context). See https://peps.python.org/pep-0572/ for more details. See also https://realpython.com/python-walrus-operator/ for a more readable explanation.
primitive_data_types: Set[PrimitiveDataType] = {
    (StringType := PrimitiveDataType("str")),
    (IntegerType := PrimitiveDataType("int")),
    (FloatType := PrimitiveDataType("float")),
    (BooleanType := PrimitiveDataType("bool")),
    (TimeType := PrimitiveDataType("time")),
    (DateType := PrimitiveDataType("date")),
    (DateTimeType := PrimitiveDataType("datetime")),
    (TimeDeltaType := PrimitiveDataType("timedelta")),
}


class EnumerationLiteral(NamedElement):
    """The `EnumerationLiteral` class represents an enumeration literal in the B-UML metamodel.

    This class inherits from the `NamedElement` class.

    Attributes
    ----------
    name : str
        The name of the enumeration literal. Inherits from `NamedElement`.

    owner : Optional[DataType]
        The owner data type of the enumeration literal. By default it is `None`.

    timestamp : datetime
        The object creation datetime. Inherits from `NamedElement`.
        By default it is set to the actual object creation time.
        See the `__init__` method for more details.

    synonyms : Optional[List[str]]
        The list of synonyms of the enumeration literal. Inherits from `NamedElement`.
        By default it is `None`.

    Parameters
    ----------
    name : str
        The name of the enumeration literal.

    owner : Optional[DataType]
        The owner data type of the enumeration literal.

    timestamp : Optional[datetime]
        The object creation datetime.

    synonyms : Optional[List[str]]
        The list of synonyms of the enumeration literal.
    """

    def __init__(
        self,
        name: str,
        owner: Optional[DataType] = None,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        """Initialize an instance of the `EnumerationLiteral` class.

        See the class docstring for more details on `Parameters` and `Attributes`.
        """
        # Initialize the `NamedElement` superclass.
        super().__init__(name, timestamp, synonyms)

        # Set the owner data type of the enumeration literal.
        self.owner: Optional[DataType] = owner

    @property
    def owner(self) -> Optional[DataType]:
        """Get the owner data type of the enumeration literal.

        Returns
        -------
        owner : Optional[DataType]
            The owner data type of the enumeration literal.
        """
        return self.__owner

    @owner.setter
    def owner(self, owner: Optional[DataType]):
        """Set the owner data type of the enumeration literal.

        Parameters
        ----------
        owner : Optional[DataType]
            The owner data type of the enumeration literal.

        Raises
        ------
        ValueError
            If the owner is an instance of `PrimitiveDataType`.
        """

        # Check if the owner is an instance of `PrimitiveDataType`.
        if isinstance(owner, PrimitiveDataType):
            raise ValueError("Invalid owner.")

        # Set the owner data type of the enumeration literal.
        self.__owner = owner

    def __repr__(self) -> str:
        """Return a string representation of the `EnumerationLiteral` object.

        The string representation includes the `name`, `owner`, `timestamp`, and `synonyms` of the `EnumerationLiteral` object.

        Returns
        -------
        str
            A string representation of the `EnumerationLiteral` object.
        """
        return f"EnumerationLiteral({self.name}, {self.owner}, {self.timestamp}, {self.synonyms})"


class Enumeration(DataType):
    """The `Enumeration` class represents an enumeration with a specified name and a set of enumeration literals in the B-UML metamodel.

    This class is a subclass of `DataType`.

    Attributes
    ----------
    name : str
        The name of the enumeration data type. Inherits from `DataType`.

    literals : Set[EnumerationLiteral]
        The set of enumeration literals associated with the enumeration. By default it is set to an empty set.
        See the `__init__` method for more details.

    timestamp : datetime
        The object creation datetime. Inherits from `DataType`.
        By default it is set to the actual object creation time.
        See the `__init__` method for more details.

    synonyms : Optional[List[str]]
        The list of synonyms of the enumeration. Inherits from `DataType`.
        By default it is `None`.

    Parameters
    ----------
    name : str
        The name of the enumeration data type.

    literals : Optional[Set[EnumerationLiteral]]
        The set of enumeration literals associated with the enumeration.

    timestamp : Optional[datetime]
        The object creation datetime.

    synonyms : Optional[List[str]]
        The list of synonyms of the enumeration.

    Methods
    -------
    add_literal(literal)
        Add an enumeration literal to the set of enumeration literals associated with the enumeration.
    """

    def __init__(
        self,
        name: str,
        literals: Optional[Set[EnumerationLiteral]] = None,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        """Initialize an instance of the `Enumeration` class.

        See the class docstring for more details on `Parameters` and `Attributes`.
        """
        # Initialize the `DataType` superclass.
        super().__init__(name, timestamp, synonyms)

        # Set the set of enumeration literals associated with the enumeration.
        self.literals: Set[EnumerationLiteral] = (
            literals if literals is not None else set()
        )

    @property
    def literals(self) -> Set[EnumerationLiteral]:
        """Get the set of enumeration literals associated with the enumeration.

        Returns
        -------
        literals : Set[EnumerationLiteral]
            The set of enumeration literals associated with the enumeration.
        """
        # Return the set of enumeration literals associated with the enumeration.
        return self.__literals

    @literals.setter
    def literals(self, literals: Optional[Set[EnumerationLiteral]]):
        """Set the set of enumeration literals associated with the enumeration.

        If the set of enumeration literals is `None`, set it to an empty set.

        Parameters
        ----------
        literals : Optional[Set[EnumerationLiteral]]
            The set of enumeration literals associated with the enumeration.

        Raises
        ------
        ValueError
            If the enumeration literal name already exists.
        """
        # Check if the set of enumeration literals is not `None`.
        if literals is not None:
            # For each enumeration literal in the set of enumeration literals.
            names = [literal.name for literal in literals]

            # Check if the enumeration literal name already exists.
            if len(names) != len(set(names)):
                raise ValueError(
                    "An enumeration cannot have two literals with the same name"
                )

            # Set the set of enumeration literals associated with the enumeration.
            for literal in literals:
                literal.owner = self
            self.__literals = literals

        # If the set of enumeration literals is `None`, set it to an empty set.
        else:
            self.__literals = set()

    def add_literal(self, literal: EnumerationLiteral):
        """Add an enumeration literal to the set of enumeration literals associated with the enumeration.

        TODO: Refer to this as `Type_Safety_of_Add_Methods` (as this issues happens in other classes as well).
        Check if this is type-safe. As the `literals` attribute is `Set[EnumerationLiteral]` (non-nullable) and has a default value of `set()`, the `add_literal` method should be type-safe (therefore "Check if the set of enumeration literals is not `None`" is not necessary). However, this should be confirmed.

        Parameters
        ----------
        literal : EnumerationLiteral
            The enumeration literal to be added to the set of enumeration literals.

        Raises
        ------
        ValueError
            If the enumeration literal name already exists.
        """
        # Check if the set of enumeration literals is not `None`.
        if self.literals is not None:
            # Check if the enumeration literal name already exists.
            if literal.name in [literal.name for literal in self.literals]:
                raise ValueError(
                    f"An enumeration cannot have two literals with the same name: '{literal.name}'"
                )

            # Add the enumeration literal to the set of enumeration literals.
            self.literals.add(literal)

    def __repr__(self) -> str:
        """Return a string representation of the `Enumeration` object.

        The string representation includes the `name`, `literals`, `timestamp`, and `synonyms` of the `Enumeration` object.

        Returns
        -------
        str
            A string representation of the `Enumeration` object.
        """
        # Return the string representation of the `Enumeration` object.
        return f"Enumeration({self.name}, {self.literals}, {self.timestamp}, {self.synonyms})"


class TypedElement(NamedElement):
    """The `TypedElement` class represents elements that have a specific type in the B-UML metamodel.

    This class inherits from `NamedElement`.

    Attributes
    ----------
    type_mapping : Dict[str, PrimitiveDataType]
        A mapping of strings to primitive data types.

    name : str
        The name of the typed element. Inherits from `NamedElement`.

    type : Type
        The data type of the typed element.
        See the `__init__` method for more details.

    timestamp : datetime
        The object creation datetime. Inherits from `NamedElement`.
        By default it is set to the actual object creation time.
        See the `__init__` method for more details.

    synonyms : Optional[List[str]]
        The list of synonyms of the typed element. Inherits from `NamedElement`.
        By default it is `None`.

    visibility : str
        Determines the kind of visibility of the typed element. Inherits from `NamedElement`.
        By default it is `public`.

    Parameters
    ----------
    name : str
        The name of the typed element.

    type : Union[Type, str]
        The data type of the typed element, as a `PrimitiveDataType` object or a string representing a primitive data type.

    timestamp : Optional[datetime]
        The object creation datetime.

    synonyms : Optional[List[str]]
        The list of synonyms of the typed element.

    visibility : str, optional
        Determines the kind of visibility of the typed element.
    """

    # Define a mapping from strings to primitive data types.
    type_mapping: Dict[str, PrimitiveDataType] = {
        "str": StringType,
        "string": StringType,
        "int": IntegerType,
        "float": FloatType,
        "bool": BooleanType,
        "time": TimeType,
        "date": DateType,
        "datetime": DateTimeType,
        "timedelta": TimeDeltaType,
    }

    def __init__(
        self,
        name: str,
        type: Union[Type, str],
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
        visibility: str = "public",
    ):
        """Initialize an instance of the `TypedElement` class.

        See the class docstring for more details on `Parameters` and `Attributes`.

        Raises
        ------
        ValueError
            If the provided type is invalid.
        """
        # Initialize the `NamedElement` superclass.
        super().__init__(name, timestamp, synonyms, visibility)

        # Set the data type of the typed element.
        # Check if the provided type is either a `Type` object or a string.
        # If it is a `Type` object, assign the provided type to the typed element.
        if isinstance(type, Type):
            # Assign the provided type to the typed element.
            self.type: Type = type

        # If the provided type is a string, check if it is a valid primitive data type. Otherwise, define a new `Type` object and assign it to the typed element.
        elif isinstance(type, str):
            # TODO: The original solution `self.type = self.type_mapping.get(type, type)` is not type-safe. This is a temporary workaround (until further decisions).
            self.type: Type = (
                self.type_mapping[type] if type in self.type_mapping else Type(type)
            )

        # If the provided type is neither a `Type` object nor a string, raise an error.
        else:
            raise ValueError("Invalid type.")

    @property
    def type(self) -> Type:
        """Get the data type of the typed element.

        Returns
        -------
        type : Type
            The data type of the typed element.
        """
        # Return the data type of the typed element.
        return self.__type

    @type.setter
    def type(self, type: Type):
        """Set the data type of the typed element.

        Parameters
        ----------
        type : Type
            The data type of the typed element.
        """
        # Set the data type of the typed element.
        self.__type = type


class Multiplicity:
    """The `Multiplicity` class represents the multiplicity of a property in the B-UML metamodel.

    Attributes
    ----------
    min : int
        The minimum multiplicity.

    max : int
        The maximum multiplicity.

    Parameters
    ----------
    min_multiplicity : int
        The minimum multiplicity.

    max_multiplicity : Union[int, str]
        The maximum multiplicity. Use "*" for unlimited.
    """

    def __init__(self, min_multiplicity: int, max_multiplicity: Union[int, str]):
        """Initialize an instance of the `Multiplicity` class.

        See the class docstring for more details on `Parameters` and `Attributes`.
        """
        # Set the minimum multiplicity.
        self.min: int = min_multiplicity

        # Set the maximum multiplicity.
        self.max: int = max_multiplicity  # type: ignore
        # Mypy does not recognize the setter decorator, but the assignment is type-safe.

    @property
    def min(self) -> int:
        """Get the minimum multiplicity.

        Returns
        -------
        min : int
            The minimum multiplicity.
        """
        # Return the minimum multiplicity.
        return self.__min

    @min.setter
    def min(self, min_multiplicity: int):
        """Set the minimum multiplicity.

        Parameters
        ----------
        min_multiplicity : int
            The minimum multiplicity.

        Raises
        ------
        ValueError
            If the minimum multiplicity is less than 0.
        """
        # Check if the minimum multiplicity is less than 0.
        if min_multiplicity < 0:
            raise ValueError("Invalid min multiplicity.")
        # Set the minimum multiplicity.
        self.__min = min_multiplicity

    @property
    def max(self) -> int:
        """Get the maximum multiplicity.

        Returns
        -------
        max : int
            The maximum multiplicity.
        """
        # Return the maximum multiplicity.
        return self.__max

    @max.setter
    def max(self, max_multiplicity: Union[int, str]):
        """Set the maximum multiplicity.

        Parameters
        ----------
        max_multiplicity : Union[int, str]
            The maximum multiplicity. Use "*" for unlimited.

        Raises
        ------
        ValueError
            If the maximum multiplicity is less than 0.

        ValueError
            If the maximum multiplicity is less than the minimum multiplicity.

        ValueError
            If the maximum multiplicity is invalid.
        """
        # Check if the maximum multiplicity is either an integer or a string.
        # If it is an integer, check if it is less than 0 and less than the minimum multiplicity.
        if isinstance(max_multiplicity, int):
            # Check if the maximum multiplicity is less than 0.
            if max_multiplicity < 0:
                raise ValueError("Invalid max multiplicity.")

            # Check if the maximum multiplicity is less than the minimum multiplicity.
            if max_multiplicity < self.min:
                raise ValueError("Invalid max multiplicity.")

            # Set the maximum multiplicity.
            self.__max = max_multiplicity

        # If the maximum multiplicity is a string, check if it is "*" or raise an error.
        elif isinstance(max_multiplicity, str):
            # Check if the maximum multiplicity is "*".
            if max_multiplicity == "*":
                # Set the maximum multiplicity.
                self.__max = UNLIMITED_MAX_MULTIPLICITY

            # If the maximum multiplicity is not "*", raise an error.
            else:
                raise ValueError("Invalid max multiplicity.")

        # If the maximum multiplicity is neither an integer nor a string, raise an error.
        else:
            raise ValueError("Invalid max multiplicity.")

    def __repr__(self) -> str:
        """Return a string representation of the `Multiplicity` object.

        The string representation includes the `min` and `max` of the `Multiplicity` object.

        Returns
        -------
        str
            A string representation of the `Multiplicity` object.
        """
        # Return the string representation of the `Multiplicity` object.
        return f"Multiplicity({self.min}, {self.max})"


# Properties are owned by a class or an association and point to a type with a multiplicity
class Property(TypedElement):
    """The `Property` class represents a attribute of a class or an end of an association in the B-UML metamodel.

    This class inherits from the `TypedElement` class.

    Attributes
    ----------
    name : str
        The name of the property. Inherits from `TypedElement`.

    type : Type
        The type of the property. Inherits from `TypedElement`.

    owner : Optional[Type]
        The type that owns the property. By default it is `None`.

    multiplicity : Multiplicity
        The multiplicity of the property. By default it is `Multiplicity(1, 1)`.

    visibility : str
        Determines the kind of visibility of the property. Inherits from `TypedElement`.
        By default it is `public`.

    is_composite : bool
        Indicates whether the property is a composite. By default it is `False`.

    is_navigable : bool
        Indicates whether the property is navigable in a relationship. By default it is `True`.

    is_id : bool
        Indicates whether the property is an id. By default it is `False`.

    is_read_only : bool
        Indicates whether the property is read only. By default it is `False`.

    timestamp : datetime
        The object creation datetime. Inherits from `TypedElement`.
        By default it is set to the actual object creation time.
        See the `__init__` method for more details.

    synonyms : List[str]
        The list of synonyms of the property. Inherits from `TypedElement`.
        By default it is `None`.

    Parameters
    ----------
    name : str
        The name of the property.

    type : Type
        The type of the property.

    owner : Optional[Type]
        The type that owns the property.

    multiplicity : Optional[Multiplicity]
        The multiplicity of the property.

    visibility : str, optional
        Determines the kind of visibility of the property.

    is_composite : bool, optional
        Indicates whether the property is a composite.

    is_navigable : bool, optional
        Indicates whether the property is navigable in a relationship.

    is_id : bool, optional
        Indicates whether the property is an id.

    is_read_only : bool, optional
        Indicates whether the property is read only.

    timestamp : Optional[datetime]
        The object creation datetime.

    synonyms : Optional[List[str]]
        The list of synonyms of the property.
    """

    def __init__(
        self,
        name: str,
        type: Type,
        owner: Optional[
            Type
        ] = None,  # TODO: The original solution `owner: Type = None` is illogical, since a property must have an owner (i.e. a class or an association). However, this temporary solution (turn `Type` into `Optional[Type]`) is for annotating nullable values (until further decisions).
        multiplicity: Multiplicity = Multiplicity(1, 1),
        visibility: str = "public",
        is_composite: bool = False,
        is_navigable: bool = True,
        is_id: bool = False,
        is_read_only: bool = False,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        """Initialize an instance of the `Property` class.

        See the class docstring for more details on `Parameters` and `Attributes`.
        """
        # Initialize the `TypedElement` superclass.
        super().__init__(name, type, timestamp, synonyms, visibility)

        # Set the owner type of the property.
        self.owner: Optional[Type] = owner

        # Set the multiplicity of the property.
        self.multiplicity: Multiplicity = multiplicity

        # Set whether the property is composite.
        self.is_composite: bool = is_composite

        # Set whether the property is navigable.
        self.is_navigable: bool = is_navigable

        # Set whether the property is an id.
        self.is_id: bool = is_id

        # Set whether the property is read only.
        self.is_read_only: bool = is_read_only

    @property
    def owner(self) -> Optional[Type]:
        """Get the owner type of the property.

        Returns
        -------
        owner : Optional[Type]
            The owner type of the property.
        """
        return self.__owner

    @owner.setter
    def owner(self, owner: Type):
        """Set the owner type of the property.

        Parameters
        ----------
        owner : Type
            The owner type of the property.

        Raises
        ------
        ValueError
            If the owner is an instance of `DataType`.
        """
        # Check if the owner is an instance of `DataType`.
        if isinstance(owner, DataType):
            raise ValueError("Invalid owner.")

        # Set the owner type of the property.
        self.__owner = owner

    @property
    def is_composite(self) -> bool:
        """
        Get whether the property is composite.

        Returns
        -------
        bool
            True if the property is composite, False otherwise.
        """
        return self.__is_composite

    @is_composite.setter
    def is_composite(self, is_composite: bool):
        """
        Set whether the property is composite.

        Parameters
        ----------
        is_composite : bool
            True if the property is composite, False otherwise.
        """
        self.__is_composite = is_composite

    @property
    def is_navigable(self) -> bool:
        """
        Get whether the property is navigable.

        Returns
        -------
        bool
            True if the property is navigable, False otherwise.
        """
        return self.__is_navigable

    @is_navigable.setter
    def is_navigable(self, is_navigable: bool):
        """
        Set whether the property is navigable.

        Parameters
        ----------
        is_navigable : bool
            True if the property is navigable, False otherwise.
        """
        self.__is_navigable = is_navigable

    @property
    def is_id(self) -> bool:
        """
        Get whether the property is an id.

        Returns
        -------
        bool
            True if the property is an id, False otherwise.
        """
        return self.__is_id

    @is_id.setter
    def is_id(self, is_id: bool):
        """
        Set whether the property is an id.

        Parameters
        ----------
        is_id : bool
            True if the property is an id, False otherwise.
        """
        self.__is_id = is_id

    @property
    def is_read_only(self) -> bool:
        """
        Get whether the property is read only.

        Returns
        -------
        bool
            True if the property is read only, False otherwise.
        """
        return self.__is_read_only

    @is_read_only.setter
    def is_read_only(self, is_read_only: bool):
        """
        Set whether the property is read only.

        Parameters
        ----------
        is_read_only : bool
            True if the property is read only, False otherwise.
        """
        self.__is_read_only = is_read_only

    def __repr__(self) -> str:
        """Return a string representation of the `Property` object.

        The string representation includes the `name`, `visibility`, `type`, `multiplicity`,
        `is_composite`, `is_id`, `is_read_only`, `timestamp`, and `synonyms` of the `Property` object.

        Returns
        -------
        str
            A string representation of the `Property` object.
        """
        return (
            f"Property({self.name}, {self.visibility}, {self.type}, {self.multiplicity}, "
            f"is_composite={self.is_composite}, is_id={self.is_id}, "
            f"is_read_only={self.is_read_only}, {self.timestamp}, {self.synonyms})"
        )


class Parameter(TypedElement):
    """The `Parameter` class represents a parameter of a method with a specific type in the B-UML metamodel.

    This class inherits from the `TypedElement` class.

    Attributes
    ----------
    name : str
        The name of the parameter. Inherits from `TypedElement`.

    type : Type
        The data type of the parameter. Inherits from `TypedElement`.

    default_value : Any
        The default value of the parameter. By default it is `None`.

    timestamp : datetime
        The object creation datetime. Inherits from `TypedElement`.
        By default it is set to the actual object creation time.
        See the `__init__` method for more details.

    synonyms : Optional[List[str]]
        The list of synonyms of the parameter. Inherits from `TypedElement`.
        By default it is `None`.

    Parameters
    ----------
    name : str
        The name of the parameter.

    type : Type
        The data type of the parameter.

    default_value : Any, optional
        The default value of the parameter.

    timestamp : Optional[datetime]
        The object creation datetime.

    synonyms : Optional[List[str]]
        The list of synonyms of the parameter.
    """

    def __init__(
        self,
        name: str,
        type: Type,
        default_value: Any = None,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        """Initialize an instance of the `Parameter` class.

        See the class docstring for more details on `Parameters` and `Attributes`.
        """
        # Initialize the `TypedElement` superclass.
        super().__init__(name, type, timestamp, synonyms)

        # Set the default value of the parameter.
        self.default_value: Any = default_value

    @property
    def default_value(self) -> Any:
        """Get the default value of the parameter.

        Returns
        -------
        default_value : Any
            The default value of the parameter.
        """
        # Return the default value of the parameter.
        return self.__default_value

    @default_value.setter
    def default_value(self, default_value: Any):
        """Set the default value of the parameter.

        Parameters
        ----------
        default_value : Any
            The default value of the parameter.
        """
        # Set the default value of the parameter.
        self.__default_value = default_value

    def __repr__(self) -> str:
        """Return a string representation of the `Parameter` object.

        The string representation includes the `name`, `type`, `default_value`, `timestamp`, and `synonyms` of the `Parameter` object.

        Returns
        -------
        str
            A string representation of the `Parameter` object.
        """
        return f"Parameter({self.name}, {self.type}, {self.default_value}, {self.timestamp}, {self.synonyms})"


class Method(TypedElement):
    """The `Method` class represents a method of a class in the B-UML metamodel.

    This class inherits from the `TypedElement` class.

    Attributes
    ----------
    name : str
        The name of the method. Inherits from `TypedElement`.

    visibility : str
        The visibility of the method. Inherits from `TypedElement`.

    is_abstract : bool
        Indicates whether the method is abstract. By default it is `False`.

    parameters : Set[Parameter]
        The set of parameters of the method. By default it is an empty set.
        See the `__init__` method for more details.

    type : Type
        The type of the method. Inherits from `TypedElement`.

    owner : Type
        The type that owns the method. By default it is `None`.

    code : str
        The code of the method. By default it is an empty string.

    timestamp : datetime
        The object creation datetime. Inherits from `TypedElement`.
        By default it is set to the actual object creation time.
        See the `__init__` method for more details.

    synonyms : Optional[List[str]]
        The list of synonyms of the method. Inherits from `TypedElement`.
        By default it is `None`.

    Parameters
    ----------
    name : str
        The name of the method.

    visibility : str, optional
        The visibility of the method.

    is_abstract : bool, optional
        Indicates whether the method is abstract.

    parameters : Optional[Set[Parameter]]
        The set of parameters of the method.

    type : Optional[Type]
        The type of the method.

    owner : Optional[Type]
        The type that owns the method.

    code : str, optional
        The code of the method.

    timestamp : Optional[datetime]
        The object creation datetime.

    synonyms : Optional[List[str]]
        The list of synonyms of the method.

    Methods
    -------
    add_parameter(parameter)
        Add a parameter to the set of parameters of the method.
    """

    def __init__(
        self,
        name: str,
        visibility: str = "public",
        is_abstract: bool = False,
        parameters: Optional[Set[Parameter]] = None,
        type: Optional[
            Type
        ] = None,  # TODO: The original solution `type: Type = None` is illogical, since a method must have a type (even if its `OclVoid`). However, this temporary solution (turn `Type` into `Optional[Type]`) is for annotating nullable values (until further decisions).
        owner: Optional[
            Type
        ] = None,  # TODO: The original solution `owner: Type = None` is illogical, since a method must have an owner (i.e. a class). However, this temporary solution (turn `Type` into `Optional[Type]`) is for annotating nullable values (until further decisions).
        code: str = "",
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        """Initialize an instance of the `Method` class.

        See the class docstring for more details on `Parameters` and `Attributes`.
        """
        # Initialize the `TypedElement` superclass.
        # TODO: As mentioned, the `type` attributes need a better definition. This is a temporary solution (until further decisions).
        super().__init__(
            name, "OclVoid" if type is None else type, timestamp, synonyms, visibility
        )

        # Set whether the method is abstract.
        self.is_abstract: bool = is_abstract

        # Set the set of parameters of the method.
        self.parameters: Set[Parameter] = (
            parameters if parameters is not None else set()
        )

        # Set the owner type of the method.
        self.owner: Optional[Type] = owner

        # Set the code of the method.
        self.code: str = code

    @property
    def is_abstract(self) -> bool:
        """Get whether the method is abstract.

        Returns
        -------
        bool
            True if the method is abstract, False otherwise.
        """
        # Return whether the method is abstract.
        return self.__is_abstract

    @is_abstract.setter
    def is_abstract(self, is_abstract: bool):
        """Set whether the method is abstract.

        Parameters
        ----------
        is_abstract : bool
            True if the method is abstract, False otherwise.
        """
        # Set whether the method is abstract.
        self.__is_abstract = is_abstract

    @property
    def parameters(self) -> Set[Parameter]:
        """Get the parameters of the method.

        Returns
        -------
        parameters : Set[Parameter]
            The parameters of the method.
        """
        return self.__parameters

    @parameters.setter
    def parameters(self, parameters: Optional[Set[Parameter]]):
        """Set the parameters of the method.

        If the set of parameters is `None`, set it to an empty set.

        Parameters
        ----------
        parameters : Optional[Set[Parameter]]
            The parameters of the method.

        Raises
        ------
        ValueError
            If the method has parameters with duplicate names.
        """
        # Check if the set of parameters is not `None`.
        if parameters is not None:
            # Define a set of names seen and a set of duplicates.
            names_seen: Set[str] = set()
            duplicates: Set[str] = set()

            # For each parameter in the set of parameters, check if the parameter name already exists.
            for parameter in parameters:
                if parameter.name in names_seen:
                    duplicates.add(parameter.name)
                names_seen.add(parameter.name)
                # Also, set the owner of the parameter to the method.
                # TODO: Check if this code below is necessary (since the `Parameter` class does not have an `owner` attribute).
                # parameter.owner = self -- Commented out for now.

            # Check if the method has parameters with duplicate names.
            if duplicates:
                raise ValueError(
                    f"A method cannot have parameters with duplicate names: {', '.join(duplicates)}."
                )

            # Set the set of parameters of the method.
            self.__parameters = parameters

        # If the set of parameters is `None`, set it to an empty set.
        else:
            self.__parameters = set()

    def add_parameter(self, parameter: Parameter):
        """Add a parameter to the set of parameters of the method.

        TODO: Refer to the `Type_Safety_of_Add_Methods` issue.

        Parameters
        ----------
        parameter : Parameter
            The parameter to be added to the set of parameters of the method.

        Raises
        ------
        ValueError
            If the method has two parameters with the same name.
        """
        # Check if the set of parameters is not `None`.
        if self.parameters is not None:
            # Check if the method has two parameters with the same name.
            if parameter.name in [parameter.name for parameter in self.parameters]:
                raise ValueError(
                    f"A method cannot have two parameters with the same name: '{parameter.name}'."
                )

            # Add the parameter to the set of parameters of the method.
            self.parameters.add(parameter)

    @property
    def owner(self) -> Optional[Type]:
        """Get the owner type of the method.

        Returns
        -------
        owner : Optional[Type]
            The owner type of the method.
        """
        return self.__owner

    @owner.setter
    def owner(self, owner: Type):
        """Set the owner type of the method.

        Parameters
        ----------
        owner : Type
            The owner type of the method.

        Raises
        ------
        ValueError
            If the owner is an instance of `DataType`.
        """
        # Check if the owner is an instance of `DataType`.
        if isinstance(owner, DataType):
            raise ValueError("Invalid owner.")

        # Set the owner type of the method.
        self.__owner = owner

    @property
    def code(self) -> str:
        """Get the code of the method.

        Returns
        -------
        code : str
            The code of the method.
        """
        return self.__code

    @code.setter
    def code(self, code: str):
        """Set the code of the method.

        Parameters
        ----------
        code : str
            The code of the method.
        """
        self.__code = code

    def __repr__(self) -> str:
        """Return a string representation of the `Method` object.

        The string representation includes the `name`, `visibility`, `is_abstract`, `parameters`,
        `type`, `owner`, `code`, `timestamp`, and `synonyms` of the `Method` object.

        Returns
        -------
        str
            A string representation of the `Method` object.
        """
        return (
            f"Method({self.name}, {self.visibility}, {self.is_abstract}, {self.parameters}, "
            f"{self.type}, {self.owner}, {self.code}, {self.timestamp}), {self.synonyms}"
        )


class Class(Type):
    """The `Class` class represents a class in the B-UML metamodel.

    A class is a type that defines a blueprint for objects. It can have attributes, associations,
    and generalizations with other classes.

    This class inherits from the `Type` class.

    TODO: Should `__associations` and `__generalizations` be named `associations` and `generalizations`?

    Attributes
    ----------
    name : str
        The name of the class. Inherits from `Type`.

    attributes : Set[Property]
        The set of attributes associated with the class. By default it is an empty set.
        See the `__init__` method for more details.

    methods : Set[Method]
        The set of methods of the class. By default it is an empty set.
        See the `__init__` method for more details.

    is_abstract : bool
        Indicates whether the class is abstract. By default it is `False`.

    is_read_only : bool
        Indicates whether the class is read only. By default it is `False`.

    timestamp : datetime
        The object creation datetime. Inherits from `Type`.
        By default it is set to the actual object creation time.
        See the `__init__` method for more details.

    __associations : Set[Association]
        Set of associations involving the class. Inherits from `Type`.
        Initialized as an empty set.

    __generalizations : Set[Generalization]
        Set of generalizations involving the class. Inherits from `Type`.
        Initialized as an empty set.

    Parameters
    ----------
    name: str
        The name of the class.

    attributes: Optional[Set[Property]]
        The set of attributes associated with the class.

    methods: Optional[Set[Method]]
        The set of methods of the class.

    is_abstract: bool, optional
        Indicates whether the class is abstract.

    is_read_only: bool, optional
        Indicates whether the class is read only.

    timestamp: Optional[datetime]
        The object creation datetime.

    synonyms: Optional[List[str]]
        The list of synonyms of the class.

    Methods
    -------
    TODO
    """

    def __init__(
        self,
        name: str,
        attributes: Optional[Set[Property]] = None,
        methods: Optional[Set[Method]] = None,
        is_abstract: bool = False,
        is_read_only: bool = False,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        # Initialize the `Type` superclass.
        super().__init__(name, timestamp, synonyms)

        # Set whether the class is abstract.
        self.is_abstract: bool = is_abstract

        # Set whether the class is read only.
        self.is_read_only: bool = is_read_only

        # Set the set of attributes associated with the class.
        self.attributes: Set[Property] = attributes if attributes is not None else set()

        # Set the set of methods of the class.
        self.methods: Set[Method] = methods if methods is not None else set()

        # Set of associations involving the class.
        self.__associations: Set[Association] = set()

        # Set of generalizations involving the class.
        self.__generalizations: Set[Generalization] = set()

    @property
    def attributes(self) -> Set[Property]:
        """Get the attributes of the class.

        Returns
        -------
        Set[Property]
            The attributes of the class
        """
        # Return the attributes of the class.
        return self.__attributes

    @attributes.setter
    def attributes(self, attributes: Optional[Set[Property]]):
        """Set the attributes of the class.

        If the set of attributes is `None`, set it to an empty set.

        Parameters
        ----------
        attributes : Set[Property]
            The attributes of the class.

        Raises
        ------
        ValueError
            If the class has attributes with duplicate names.

        ValueError
            If the class has more than one attribute marked as 'id'.
        """
        # Check if the set of attributes is not `None`.
        if attributes is not None:
            # Define a set of names seen and a set of duplicates, and a counter for the number of 'id' attributes.
            names_seen = set()
            duplicates = set()
            id_counter = 0

            # For each attribute in the set of attributes, check if the attribute name already exists.
            for attribute in attributes:
                if attribute.name in names_seen:
                    duplicates.add(attribute.name)
                names_seen.add(attribute.name)

                # Also, check if the attribute is marked as 'id'.
                if attribute.is_id:
                    id_counter += 1

            # Check if the class has attributes with duplicate names.
            if duplicates:
                raise ValueError(
                    f"A class cannot have attributes with duplicate names: {', '.join(duplicates)}."
                )

            # Check if the class has more than one attribute marked as 'id'.
            if id_counter > 1:
                raise ValueError(
                    "A class cannot have more than one attribute marked as 'id'."
                )

            # Set the set of attributes of the class.
            for attribute in attributes:
                attribute.owner = self
            self.__attributes = attributes

        # If the set of attributes is `None`, set it to an empty set.
        else:
            self.__attributes = set()

    @property
    def methods(self) -> Set[Method]:
        """Get the methods of the class.

        Returns
        -------
        set[Method]
            The methods of the class.
        """
        # Return the methods of the class.
        return self.__methods

    @methods.setter
    def methods(self, methods: Set[Method]):
        """Set the methods of the class.

        If the set of methods is `None`, set it to an empty set.

        Parameters
        ----------
        methods : set[Method]
            The methods of the class.

        Raises
        ------
        ValueError
            If the class has methods with duplicate names.
        """
        # Check if the set of methods is not `None`.
        if methods is not None:
            # Define a set of names seen and a set of duplicates.
            names_seen = set()
            duplicates = set()

            # For each method in the set of methods, check if the method name already exists.
            for method in methods:
                if method.name in names_seen:
                    duplicates.add(method.name)
                names_seen.add(method.name)

            # Check if the class has methods with duplicate names.
            if duplicates:
                raise ValueError(
                    f"A class cannot have methods with duplicate names: {', '.join(duplicates)}."
                )

            # Set the set of methods of the class.
            for method in methods:
                method.owner = self
            self.__methods = methods

        # If the set of methods is `None`, set it to an empty set.
        else:
            self.__methods = set()

    def add_method(self, method: Method):
        """Add a method to the set of methods of the class.

        TODO: Refer to the `Type_Safety_of_Add_Methods` issue.

        Parameters
        ----------
        method : Method
            The method to be added to the set of methods of the class.

        Raises
        ------
        ValueError
            If the class has two methods with the same name.
        """
        # Check if the set of methods is not `None`.
        if self.methods is not None:
            if method.name in [method.name for method in self.methods]:
                raise ValueError(
                    f"A class cannot have two methods with the same name: '{method.name}'."
                )
            method.owner = self
            self.methods.add(method)

    def all_attributes(self) -> set[Property]:
        """set[Property]: Get all attributes, including inherited ones."""
        inherited_attributes: set[Property] = self.inherited_attributes()
        return self.__attributes | inherited_attributes

    def add_attribute(self, attribute: Property):
        """
        Property: Add an attribute to the set of class attributes.

        TODO: Refer to the `Type_Safety_of_Add_Methods` issue.

        Raises:
            ValueError: if the attribute name already exist.
        """
        if self.attributes is not None:
            if attribute.name in [attribute.name for attribute in self.attributes]:
                raise ValueError(
                    f"A class cannot have two attributes with the same name: '{attribute.name}'."
                )
            attribute.owner = self
            self.attributes.add(attribute)

    @property
    def is_abstract(self) -> bool:
        """Get whether the class is abstract.

        Returns
        -------
        bool
            True if the class is abstract, False otherwise.
        """
        # Return whether the class is abstract.
        return self.__is_abstract

    @is_abstract.setter
    def is_abstract(self, is_abstract: bool):
        """Set whether the class is abstract.

        Parameters
        ----------
        is_abstract : bool
            True if the class is abstract, False otherwise.
        """
        # Set whether the class is abstract.
        self.__is_abstract = is_abstract

    @property
    def is_read_only(self) -> bool:
        """Get whether the class is read only.

        Returns
        -------
        bool
            True if the class is read only, False otherwise.
        """
        # Return whether the class is read only.
        return self.__is_read_only

    @is_read_only.setter
    def is_read_only(self, is_read_only: bool):
        """Set whether the class is read only.

        Parameters
        ----------
        is_read_only : bool
            True if the class is read only, False otherwise.
        """
        self.__is_read_only = is_read_only

    @property
    def associations(self) -> set:
        """set[Association]: Get the set of associations involving the class."""
        return self.__associations

    def _add_association(self, association):
        """Association: Add an association to the set of class associations."""
        self.__associations.add(association)

    def _delete_association(self, association):
        """Association: Remove an association to the set of class associations."""
        self.__associations.discard(association)

    @property
    def generalizations(self) -> set:
        """set[Generalization]: Get the set of generalizations involving the class."""
        return self.__generalizations

    def _add_generalization(self, generalization):
        """Generalization: Add a generalization to the set of class generalizations."""
        self.__generalizations.add(generalization)

    def _delete_generalization(self, generalization):
        """Generalization: Remove a generalization to the set of class generalizations."""
        self.__generalizations.discard(generalization)

    def inherited_attributes(self) -> set[Property]:
        """set[Property]: Get the set of inherited attributes."""
        inherited_attributes = set()
        for parent in self.all_parents():
            inherited_attributes.update(parent.attributes)
        return inherited_attributes

    def association_ends(self) -> set:
        """set[Property]: Get the set of association ends of the class."""
        ends = set()
        for association in self.__associations:
            aends = association.ends
            ends.update(aends)
            l_aends = list(aends)
            if not (len(l_aends) == 2 and l_aends[0].type == l_aends[1].type):
                for end in aends:
                    if end.type == self:
                        ends.discard(end)
        return ends

    def all_association_ends(self) -> set[Property]:
        """set[Property]: Get the set of direct and indirect association ends of the class."""
        all_ends = self.association_ends()
        for parent in self.all_parents():
            ends = parent.association_ends()
            all_ends.update(ends)
        return all_ends

    def parents(self) -> set:
        """set[Class]: Get the set of direct parents of the class."""
        parents = set()
        for generalization in self.__generalizations:
            if generalization.general != self:
                parents.add(generalization.general)
        return parents

    def all_parents(self) -> set:
        """set[Class]: Get the set of direct and indirect parents of the class."""
        all_parents = set()
        all_parents.update(self.parents())
        for parent in self.parents():
            all_parents.update(parent.all_parents())
        return all_parents

    def specializations(self) -> set:
        """set[Class]: Get the set of direct specializations (children) of the class."""
        specializations = set()
        for generalization in self.__generalizations:
            if generalization.specific != self:
                specializations.add(generalization.specific)
        return specializations

    def all_specializations(self) -> set:
        """set[Class]: Get the set of direct and indirect specializations (children) of the class."""
        all_spec = set()
        all_spec.update(self.specializations())
        for specialization in self.specializations():
            all_spec.update(specialization.all_specializations())
        return all_spec

    def id_attribute(self) -> Property:
        """Property: Get the id attribute of the class."""
        for attribute in self.attributes:
            if attribute.is_id:
                return attribute
        return None

    def __repr__(self):
        return f"Class({self.name}, {self.attributes}, {self.methods}, {self.timestamp}, {self.synonyms})"


class Association(NamedElement):
    """Represents an association between classes.

    An Association defines a relationship between classes and is composed of two or more ends,
    each associated with a class. An association must have more than one end.

    Args:
        name (str): The name of the association.
        ends (set[Property]): The set of ends related to the association.
        timestamp (datetime): Object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the association (None as default).

    Attributes:
        name (str): Inherited from NamedElement, represents the name of the association.
        ends (set[Property]): The set of ends related to the association.
        timestamp (datetime): Inherited from NamedElement; object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the association (None as default).
    """

    def __init__(
        self,
        name: str,
        ends: set[Property],
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        super().__init__(name, timestamp, synonyms)
        self.ends: set[Property] = ends

    @property
    def ends(self) -> set[Property]:
        """set[Property]: Get the ends of the association."""
        return self.__ends

    @ends.setter
    def ends(self, ends: set[Property]):
        """
        set[Property]: Set the ends of the association. Two or more ends are required.

        Raises:
            ValueError: if an association has less than two ends.
        """
        if len(ends) <= 1:
            raise ValueError("An association must have more than one end.")
        if hasattr(self, "ends"):
            for end in self.ends:
                end.type._delete_association(association=self)
        for end in ends:
            end.owner = self
            end.type._add_association(association=self)
        self.__ends = ends

    def __repr__(self):
        return (
            f"Association({self.name}, {self.ends}, {self.timestamp}, {self.synonyms})"
        )


class BinaryAssociation(Association):
    """Represents a binary association between two classes.

    A BinaryAssociation is a specialized form of Association that specifically involves
    two ends, each associated with a class. It enforces constraints on the association,
    such as having exactly two ends. Exactly two ends are required

    Args:
        name (str): The name of the binary association.
        ends (set[Property]): The set of ends related to the binary association.
        timestamp (datetime): Object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the binary association (None as default).

    Attributes:
        name (str): Inherited from Association, represents the name of the binary association.
        ends (set[Property]): Inherited from NamedElement, represents the set of ends related to the binary association.
        timestamp (datetime): Inherited from NamedElement; object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the binary association (None as default).
    """

    @Association.ends.setter
    def ends(self, ends: set[Property]):
        """set[Property]: Set the ends of the association.

        Raises:
            ValueError: if the associaiton ends are not exactly two, or if both ends are tagged as agregation, or
            if both ends are tagged as composition.
        """
        if len(ends) != 2:
            raise ValueError("A binary association must have exactly two ends.")
        if list(ends)[0].is_composite is True and list(ends)[1].is_composite is True:
            raise ValueError("The composition attribute cannot be tagged at both ends.")
        super(BinaryAssociation, BinaryAssociation).ends.fset(self, ends)

    def __repr__(self):
        return f"BinaryAssociation({self.name}, {self.ends}, {self.timestamp}, {self.synonyms})"


class AssociationClass(Class):
    # Class that has an association nature
    """An AssociationClass is a class that that has an association nature.
    It inherits from Class and is associated with an underlying Association.

    Args:
        name (str): The name of the association class.
        attributes (set[Property]): The set of attributes associated with the association class.
        association (Association): The underlying association linked to the association class.
        timestamp (datetime): Object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the association class (None as default).

    Attributes:
        name (str): Inherited from Class, represents the name of the association class.
        attributes (set[Property]): Inherited from Class, represents the set of attributes associated with the association class.
        association (Association): The underlying association linked to the association class.
        timestamp (datetime): Inherited from NamedElement; object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the association class (None as default).
    """

    def __init__(
        self,
        name: str,
        attributes: set[Property],
        association: Association,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        super().__init__(name, attributes, timestamp, synonyms)
        self.association: Association = association

    @property
    def association(self) -> Association:
        """Association: Get the underlying association of the association class."""
        return self.__association

    @association.setter
    def association(self, association: Association):
        """Association: Set the underlying association of the association class."""
        self.__association = association

    def __repr__(self):
        return f"AssociationClass({self.name}, {self.attributes}, {self.association}, {self.timestamp}, {self.synonyms})"


class Generalization(Element):
    """Represents a generalization relationship between two classes.

    A Generalization is a relationship between two classes, where one class (specific)
    inherits attributes and behaviors from another class (general).

    Args:
        general (Class): The general (parent) class in the generalization relationship.
        specific (Class): The specific (child) class in the generalization relationship.
        timestamp (datetime): Object creation datetime (default is current time).

    Attributes:
        general (Class): The general (parent) class in the generalization relationship.
        specific (Class): The specific (child) class in the generalization relationship.
        timestamp (datetime): Inherited from NamedElement; object creation datetime (default is current time).
    """

    def __init__(
        self, general: Class, specific: Class, timestamp: Optional[datetime] = None
    ):
        self.general: Class = general
        self.specific: Class = specific
        self.timestamp: datetime = timestamp

    @property
    def general(self) -> Class:
        """Class: Get the general (parent) class."""
        return self.__general

    @general.setter
    def general(self, general: Class):
        """Class: Set the general (parent) class."""
        if hasattr(self, "general"):
            self.general._delete_generalization(generalization=self)
        general._add_generalization(generalization=self)
        self.__general = general

    @property
    def specific(self) -> Class:
        """Class: Get the specific (child) class."""
        return self.__specific

    @specific.setter
    def specific(self, specific: Class):
        """
        Class: Set the specific (child) class.

        Raises:
            ValueError: if the general class is equal to the specific class
        """
        if specific == self.general:
            raise ValueError("A class cannot be a generalization of itself.")
        if hasattr(self, "specific"):
            self.specific._delete_generalization(generalization=self)
        specific._add_generalization(generalization=self)
        self.__specific = specific

    @property
    def timestamp(self) -> datetime:
        """str: Get the timestamp of the generalization."""
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        """str: Set the timestamp of the generalization."""
        self.__timestamp = timestamp

    def __repr__(self):
        return f"Generalization({self.general}, {self.specific}, {self.timestamp})"


class GeneralizationSet(NamedElement):
    """Represents a set of generalization relationships.

    Args:
        name (str): The name of the generalization set.
        generalizations (set[Generalization]): The set of generalization relationships in the set.
        is_disjoint (bool): Indicates whether the set is disjoint (instances cannot belong to more than one class
            in the set).
        is_complete (bool): Indicates whether the set is complete (every instance of the superclass must belong to
            a subclass).
        timestamp (datetime): Object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the generalization set (None as default).

    Attributes:
        name (str): Inherited from NamedElement, represents the name of the generalization set.
        generalizations (set[Generalization]): The set of generalization relationships in the set.
        is_disjoint (bool): Indicates whether the set is disjoint (instances cannot belong to more than one class
            in the set).
        is_complete (bool): Indicates whether the set is complete (every instance of the superclass must belong to
            a subclass).
        timestamp (datetime): Inherited from NamedElement; object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the generalization set (None as default).
    """

    def __init__(
        self,
        name: str,
        generalizations: set[Generalization],
        is_disjoint: bool,
        is_complete: bool,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        super().__init__(name, timestamp, synonyms)
        self.generalizations: set[Generalization] = generalizations
        self.is_disjoint: bool = is_disjoint
        self.is_complete: bool = is_complete

    @property
    def generalizations(self) -> set[Generalization]:
        """set[Generalization]: Get the generalization relationships."""
        return self.__generalizations

    @generalizations.setter
    def generalizations(self, generalizations: set[Generalization]):
        """set[Generalization]: Set the generalization relationships."""
        self.__generalizations = generalizations

    @property
    def is_disjoint(self) -> bool:
        """bool: Get whether the set is disjoint."""
        return self.__is_disjoint

    @is_disjoint.setter
    def is_disjoint(self, is_disjoint: bool):
        """bool: Set whether the set is disjoint."""
        self.__is_disjoint = is_disjoint

    @property
    def is_complete(self) -> bool:
        """bool: Get whether the set is complete."""
        return self.__is_complete

    @is_complete.setter
    def is_complete(self, is_complete: bool):
        """bool: Set whether the set is complete."""
        self.__is_complete = is_complete

    def __repr__(self):
        return (
            f"GeneralizationSet({self.name}, {self.generalizations}, "
            f"is_disjoint={self.is_disjoint}, is_complete={self.is_complete}, {self.timestamp}, {self.synonyms})"
        )


class Package(NamedElement):
    """A Package is a grouping mechanism that allows organizing and managing a set of classes.

    Attributes:
        name (str): The name of the package.
        classes (set[Class]): The set of classes contained in the package.
        timestamp (datetime): Object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the package (None as default).

    Attributes:
        name (str): Inherited from NamedElement, represents the name of the package.
        classes (set[Class]): The set of classes contained in the package.
        timestamp (datetime): Inherited from NamedElement; object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the package (None as default).
    """

    def __init__(
        self,
        name: str,
        classes: set[Class],
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        super().__init__(name, timestamp, synonyms)
        self.classes: set[Class] = classes

    @property
    def classes(self) -> set[Class]:
        """set[Class]: Get the classes contained in the package."""
        return self.__classes

    @classes.setter
    def classes(self, classes: set[Class]):
        """set[Class]: Set the classes contained in the package."""
        self.__classes = classes

    def __repr__(self):
        return (
            f"Package({self.name}, {self.classes}), {self.timestamp}, {self.synonyms}"
        )


class Constraint(NamedElement):
    """A Constraint is a statement that restricts or defines conditions on the behavior,
    structure, or other aspects of the modeled system.

    Args:
        name (str): The name of the constraint.
        context (Class): The class to which the constraint is associated.
        expression (str): The expression or condition defined by the constraint.
        language (str): The language in which the constraint expression is written.
        timestamp (datetime): Object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the constraint (None as default).

    Attributes:
        name (str): Inherited from NamedElement, represents the name of the constraint.
        context (Class): The class to which the constraint is associated.
        expression (str): The expression or condition defined by the constraint.
        language (str): The language in which the constraint expression is written.
        timestamp (datetime): Inherited from NamedElement; object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the constraint (None as default).
    """

    def __init__(
        self,
        name: str,
        context: Class,
        expression: Any,
        language: str,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        super().__init__(name, timestamp, synonyms)
        self.context: Class = context
        self.expression: str = expression
        self.language: str = language

    @property
    def context(self) -> Class:
        """Class: Get the class to which the constraint is associated."""
        return self.__context

    @context.setter
    def context(self, context: Class):
        """Class: Set the class to which the constraint is associated."""
        self.__context = context

    @property
    def expression(self) -> str:
        """str: Get the expression or condition defined by the constraint."""
        return self.__expression

    @expression.setter
    def expression(self, expression: Any):
        """str: Set the expression or condition defined by the constraint."""
        self.__expression = expression

    @property
    def language(self) -> str:
        """str: Get the language in which the constraint expression is written."""
        return self.__language

    @language.setter
    def language(self, language: str):
        """str: Set the language in which the constraint expression is written."""
        self.__language = language

    def __repr__(self):
        return f"Constraint({self.name}, {self.context.name}, {self.language}, {self.expression}, {self.timestamp})"


class Model(NamedElement):
    """A model is the root element. A model is the root element. There are different types of models
    that inherit from this class. For example, DomainModel, ObjectModel, or GUIModel.

    Args:
        name (str): The name of the model.
        timestamp (datetime): Object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the model (None as default).

    Attributes:
        name (str): Inherited from NamedElement, represents the name of the model.
        timestamp (datetime): Inherited from NamedElement; object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the model (None as default).
    """

    def __init__(
        self,
        name: str,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        super().__init__(name, timestamp, synonyms)


class DomainModel(Model):
    """A domain model comprises a number of types, associations,
    generalizations, packages, constraints, and others.

    Args:
        name (str): The name of the domain model.
        types (set[Type]): The set of types (classes and datatypes) in the domain model (set() as default).
        associations (set[Association]): The set of associations in the domain model (set() as default).
        generalizations (set[Generalization]): The set of generalizations in the domain model (set() as default).
        packages (set[Package]): The set of packages in the domain model (set() as default).
        constraints (set[Constraint]): The set of constraints in the domain model (set() as default).
        timestamp (datetime): Object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the domain model (None as default).

    Attributes:
        name (str): Inherited from NamedElement, represents the name of the domain model.
        types (set[Type]): The set of types (classes and datatypes) in the domain model (set() as default).
        associations (set[Association]): The set of associations in the domain model (set() as default).
        generalizations (set[Generalization]): The set of generalizations in the domain model (set() as default).
        packages (set[Package]): The set of packages in the domain model (set() as default).
        constraints (set[Constraint]): The set of constraints in the domain model (set() as default).
        timestamp (datetime): Inherited from NamedElement; object creation datetime (default is current time).
        synonyms (List[str]): List of synonyms of the domain model (None as default).
    """

    def __init__(
        self,
        name: str,
        types: set[Type] = None,
        associations: set[Association] = None,
        generalizations: set[Generalization] = None,
        packages: set[Package] = None,
        constraints: set[Constraint] = None,
        timestamp: Optional[datetime] = None,
        synonyms: Optional[List[str]] = None,
    ):
        super().__init__(name, timestamp, synonyms)
        self.types: set[Type] = types if types is not None else set()
        self.packages: set[Package] = packages if packages is not None else set()
        self.constraints: set[Constraint] = (
            constraints if constraints is not None else set()
        )
        self.associations: set[Association] = (
            associations if associations is not None else set()
        )
        self.generalizations: set[Generalization] = (
            generalizations if generalizations is not None else set()
        )

    @property
    def types(self) -> set[Type]:
        """set[Type]: Get the set of types in the domain model."""
        return self.__types

    @types.setter
    def types(self, types: set[Type]):
        """
        set[Type]: Set the set of types in the domain model, including primitive data types.

        Raises:
            ValueError: if there are two types with the same name.
        """
        types = types | primitive_data_types
        names_seen = set()
        duplicates = set()

        for type_ in types:
            if type_.name in names_seen:
                duplicates.add(type_.name)
            names_seen.add(type_.name)

        if duplicates:
            raise ValueError(
                f"The model cannot have types with duplicate names: {', '.join(duplicates)}."
            )
        self.__types = types

    def get_type_by_name(self, type_name: str) -> Type:
        """Type: Gets an Type by name."""
        return next(
            (
                type_element
                for type_element in self.types
                if type_element.name == type_name
            ),
            None,
        )

    def add_type(self, type_: Type):
        """Type: Add a type (Class or DataType) to the set of types of the model."""
        self.types = self.types | {type_}

    @property
    def associations(self) -> set[Association]:
        """set[Association]: Get the set of associations in the domain model."""
        return self.__associations

    @associations.setter
    def associations(self, associations: set[Association]):
        """
        set[Association]: Set the set of associations in the domain model.

        Raises:
            ValueError: if there are two associations with the same name.
        """
        if associations is not None:
            names_seen = set()
            duplicates = set()

            for association in associations:
                if association.name in names_seen:
                    duplicates.add(association.name)
                names_seen.add(association.name)

            if duplicates:
                raise ValueError(
                    f"The model cannot have associations with duplicate names: {', '.join(duplicates)}."
                )

            self.__associations = associations
        else:
            self.__associations = set()

    def add_association(self, association: Association):
        """Association: Add an association to the set of associations of the model."""
        self.associations = self.associations | {association}

    @property
    def generalizations(self) -> set[Generalization]:
        """set[Generalization]: Get the set of generalizations in the domain model."""
        return self.__generalizations

    @generalizations.setter
    def generalizations(self, generalizations: set[Generalization]):
        """set[Generalization]: Set the set of generalizations in the domain model."""
        if generalizations is not None:
            self.__generalizations = generalizations
        else:
            self.__generalizations = set()

    def add_generalization(self, generalization: Generalization):
        """Generalization: Add a generalization to the set of generalizations of the model."""
        self.generalizations = self.generalizations | {generalization}

    def get_enumerations(self) -> set[Enumeration]:
        """set[Enumeration]: Get the set of enumerations in the domain model."""
        return {element for element in self.types if isinstance(element, Enumeration)}

    @property
    def packages(self) -> set[Package]:
        """set[Package]: Get the set of packages in the domain model."""
        return self.__packages

    @packages.setter
    def packages(self, packages: set[Package]):
        """
        set[Package]: Get the set of packages in the domain model.

        Raises:
            ValueError: if there are two packages with the same name.
        """
        if packages is not None:
            names_seen = set()
            duplicates = set()

            for package in packages:
                if package.name in names_seen:
                    duplicates.add(package.name)
                names_seen.add(package.name)

            if duplicates:
                raise ValueError(
                    f"The model cannot have packages with duplicate names: {', '.join(duplicates)}."
                )

            self.__packages = packages
        else:
            self.__packages = set()

    @property
    def constraints(self) -> set[Constraint]:
        """set[Constraint]: Get the set of constraints in the domain model."""
        return self.__constraints

    @constraints.setter
    def constraints(self, constraints: set[Constraint]):
        """
        set[Constraint]: Get the set of constraints in the domain model.

        Raises:
            ValueError: if there are two constraints with the same name.
        """
        if constraints is not None:
            names = [constraint.name for constraint in constraints]
            if len(names) != len(set(names)):
                raise ValueError(
                    "The model cannot have two constraints with the same name."
                )
            self.__constraints = constraints
        else:
            self.__constraints = set()

    def get_classes(self) -> set[Class]:
        """set[Class]: Get all classes within the domain model."""
        return {element for element in self.types if isinstance(element, Class)}

    def get_class_by_name(self, class_name: str) -> Class:
        """Class: Gets a class by name."""
        return next(
            (
                element
                for element in self.types
                if isinstance(element, Class) and element.name == class_name
            ),
            None,
        )

    def classes_sorted_by_inheritance(self) -> list[Class]:
        """list[Class]: Get the list of classes ordered by inheritance."""
        classes = self.get_classes()
        # Set up a dependency graph
        child_map = {cl: set() for cl in classes}
        # Populating the child_map based on generalizations (edges in top-sort graph)
        for cl in classes:
            for generalization in cl.generalizations:
                child_map[generalization.general].add(cl)

        # Helper function for DFS
        def dfs(cl, visited, sorted_list):
            visited.add(cl)
            for child in child_map[cl]:
                if child not in visited:
                    dfs(child, visited, sorted_list)
            sorted_list.append(cl)

        # Perform DFS from each node that hasn't been visited yet
        visited = set()
        sorted_list = []
        for cl in classes:
            if cl not in visited:
                dfs(cl, visited, sorted_list)
        sorted_list.reverse()
        return sorted_list

    def __repr__(self):
        return (
            f"Package({self.name}, {self.types}, {self.associations}, {self.generalizations}, "
            f"{self.packages}, {self.constraints}, {self.timestamp}, {self.synonyms})"
        )
