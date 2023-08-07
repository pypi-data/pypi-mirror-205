## Loops

A convenient Python wrapper for the [Lopps](https://loops.so/) API.
- API docs: [https://tryloops.notion.site/API-5b453a52dd7c4b419aa4647410de9770](https://tryloops.notion.site/API-5b453a52dd7c4b419aa4647410de9770)

### Examples

#### Setup
```
from loopsso import LoopsClient
client = LoopsClinet('YOUR-API-KEY')

```
### Contacts Usage
#### Create/Add
```
client.create( 
    email='adam@loops.so',
    firstName='Adam',
    lastName='Kaczmarek',
    favoriteColor='blue',
    userGroup='Founders',
    source='Signup form Service'
    )

```

#### Update
```
client.update( 
    email='adam@loops.so',
    firstName='Adam',
    lastName='Kaczmarek',
    favoriteColor='blue',
    userGroup='Founders',
    source='Signup form Service'
    )

```

#### Find
```
client.find(email='adam@loops.so', user_id='SomeUserId')

```
#### Delete
```
client.delete(email='adam@loops.so')

```

#### Send
```
client.send(email='adam@loops.so', event_name='conversion')

```

