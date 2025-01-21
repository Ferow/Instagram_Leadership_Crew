from typing import Type

from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import pymssql
import os
from dotenv import load_dotenv
load_dotenv()

class SQLServerSearchToolInput(BaseModel):
    """Input schema for SQLServerToolInput."""
    procedure_name: str = Field(..., description="stored procedure name")
    parameters: dict = Field(..., description="parameters to pass to the stored procedure, must be in parameter name value format")
    
class SQLServerSearchToolOutput(BaseModel):
    """Output schema for SQLServerToolOutput."""
    output_data: dict

class SqlServerSearchTool(BaseTool):
    name: str = "SQL Server Tool"
    description: str = (
        "This tool will be used to pass information into a speciic SQL Server database's stored procedure."
    )
    args_schema: Type[BaseModel] = SQLServerSearchToolInput

    def _run(self, 
             procedure_name: str,
             parameters: dict) -> SQLServerSearchToolOutput:
        """
            Calls a stored procedure and returns the result.

            :param connection_params: Dictionary containing database connection parameters.
            :param proc_name: Name of the stored procedure to call.
            :param param_map: Dictionary mapping parameter names to their values.
            :return: List of results from the stored procedure.
        """
        server = os.getenv("SQL_SERVER")
        database = os.getenv("SQL_DATABASE") 
        user = os.getenv("SQL_USERNAME")
        password = os.getenv("SQL_PASSWORD")
        print("Here's the creds")
        print (server, database, user, password)
        connection_params = {
      
        }

        results = []

        conn = pymssql.connect(
            server='FROAISURFACEBOO\FROSQL',
            user= 'CREWAI',
            password= 'Grace$2482599669',
            database= 'INSTAGRAM_LEADERSHIP',
            as_dict=True
        )
          
        # Stored procedure name and parameters
        #proc_name = "WeeklyThemes_GetThemeByDate"
        param_map = {"@SearchDate": "2025-01-01"}   

        try:
            # Connect to the database
            with conn.cursor() as cursor:  # Use as_dict=True to get results as dictionaries
                # Map dictionary values to the stored procedure parameters
                params = tuple(param_map.values())
                
                # Call the stored procedure
                cursor.callproc(procedure_name, params)
                
                # Fetch all results
                results = cursor.fetchall()
                
                # Parse results into a dictionary
                parsed_results = [{key: value for key, value in row.items()} for row in results]

                # If no data is returned, add a record to the dictionary with a message
                if not parsed_results:
                    parsed_results = [{"No data found": "No data found"}]

        except pymssql.Error as e:
            print(f"Error while calling stored procedure: {e}")
            parsed_results = ["No data returned", "Error while producing results"]

        return SQLServerSearchToolOutput(output_data=parsed_results)
   
