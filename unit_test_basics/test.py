'''
Mocking a method that is being used in another method. PS: The method can also have multiple API calls.
'''
from unittest.mock import Mock

#response we expect
data = [{"test": "test"}]
#make an object of the class
obj = Service(config={})
#use the object of the class DOT(.) the method name = Mock(return_value=[])
obj.api_data = Mock(return_value=data)
#now run the method that calls the other method we mocked
ans = obj.run()


