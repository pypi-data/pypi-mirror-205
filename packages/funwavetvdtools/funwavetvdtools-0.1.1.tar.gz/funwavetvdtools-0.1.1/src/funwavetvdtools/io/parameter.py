##
# @file inputfile.py
#
# @brief Interface for FUNWAVE-TVD input/driver text file.
#
# @section description_inputfile Description
# Example Python program with Doxygen style comments.
#
# @section libraries_main Libraries/Modules
# - enum standard library (https://https://docs.python.org/3/library/enum.html)
#   - Access to enumeration functionality.
# - pandas library (https://pandasguide.readthedocs.io/en/latest/)
#   - Access to parsing CSV files.
#
# @section notes_inputfile Notes
# - Comments are Doxygen compatible.
#
# @section todo_doxygen_example TODO
# - None.
#
# @section author_doxygen_example Author(s)
# - Created by Michael-Angelo Y.-H. Lam on 04/29/2022.
#
# Copyright (c) 2022 FUNWAVE-TVD Group.  All rights reserved.

from enum import Enum
import pandas as pd

class Datatype(Enum):
    """Datatype enumeration for Parameter class."""
    
    #: String
    STRING  = 1
    #: Float/Double
    FLOAT   = 2
    #: Integer
    INTEGER = 3
    #: Path String
    PATH    = 4

class Validation(Enum):
    NONE=1,
    RANGE=2,
    POSTIVE=3,
    NONNEGATIVE=4

def formatValueByDataType( val , datatype ):   
    
    if datatype == Datatype.STRING : return str(val)
    if datatype == DataType.PATH   : return str(val)
    if datatype == Datatype.INTEGER: return int(val)
    if datatype == Datatype.FLOAT  : return float(val)
    
    raise Exception( "Datatype '%s' conversion not implement" % datatype._name_ )
    
    
class Category(Enum):
    """Parameter class category/subtype enumeration."""
    #: Generic parameters for central FUNWAVE-TVD module
    GENERAL    = 1
    #: Grid/spatial specific parameters for central FUNWAVE-TVD module
    GRID       = 2
    #: Temportal specific parameters for central FUNWAVE-TVD module
    TIME       = 3
    #: Numerical scheme parameters for central FUNWAVE-TVD module
    NUMERICS   = 4
    #: Parameters for optional Vessel FUNWAVE-TVD module
    VESSEL     = 5
    #: Parameters for optional Sediment transport FUNWAVE-TVD module
    SEDIMENT   = 6
    #: Parameters for optional meteotsunamis FUNWAVE-TVD module
    METEO      = 7
    #: Partmeters for optional Lagrangian particle tracking FUNWAVE-TVD module
    LAGRANGIAN = 8
    
class Parameter:

    """Class for interfacing with FUNWAVE input file parameter.
 
    :param name:         Name of parameter in FUNWAVE-TVD input file.
    :type  name:          str
    :param fullname:     Descriptive name for parameter.
    :type  fullname:      str
    :param datatype:     Datatype Enum value for parameter datatype
    :type  datatype:      Datatype
    :param category:     Category Enum value for parameter subttype.
    :type  category:      Category
    :param isRequired:   Logical denoting if parameter is required for FUNWAVE-TVD execution.
    :type  isRequired:    bool
    :param description:  Detail text description of parameter
    :type  description:   str
    :param defaultValue: Optional default value of parameter 
    :type  defaultValue:  any
    """
    def __init__(self, name, fullname, datatype, category, is_required, description, default_value=None):
        #: Doc comment for instance attribute qux.
        self._name          = name
        self._fullname      = fullname
        self._datatype      = datatype
        self._category      = category
        self._description   = description
        self._is_required   = is_required
        self._default_value = default_value
        self._value         = default_value

    @property
    def name(self):
        """Getter/property for FUNWAVE-TVD name of.

        :rtype: str
        """
        return self._name
    @property
    def fullname(self):
        """Getter/property for descriptive name.

        :rtype: str
        """
        return self._fullname

    @property
    def datatype(self):
        """Getter/property for Datatype Enum value.

        :rtype: Datatype
        """
        return self._datatype

    @property
    def category(self):
        """Getter/property for Category Enum value.

        :rtype: Category
        """
        return self._category

    @property
    def description(self):
        """Getter/property for description text.

        :rtype: str
        """
        return self._description

    @property
    def is_required(self):
        """Getter/property for is required for simulation logical.

        :rtype: bool
        """
        return self._is_required

    @property
    def default_value(self):
        """Getter/property for default value.

        :rtype: object
        """
        return self._default_value

 
            
class Parameters:

    def __init__(self):
        self._parameters = []

    @property
    def parameters(self): return self._parameters








 
            
