# Slim-ID: A Lightweight ID Generation Library for Python

下の方に日本語の説明があります

## Overview
- This is a tool that automatically generates short IDs.
- It has a mechanism to avoid collisions with already generated IDs.

## Features
- Specify the desired length for generated IDs (default is 5 characters)
- Automatically increases the length if the generated ID conflicts with existing IDs
- Specify the alphabet to use for the ID (default is URL-safe Base64, but hexadecimal can also be specified)
- Uses cryptographically secure random number generation internally, providing a degree of protection against attackers predicting the random number from timestamps, etc.
- Requires a user-defined function to determine if a generated ID conflicts with existing IDs. This function is expected to handle dictionary lookups or database queries, for example.

## Usage Example
```python
import sys
import slim_id

id_dic = {}

def is_exists(arg_id):
    return (arg_id in id_dic)

# Generate an ID using Slim-ID
s_id = slim_id.gen(is_exists)
id_dic[s_id] = True
print(s_id)

# Generate an ID using Slim-ID with custom parameters
s_id = slim_id.gen(
    is_exists,  # Function to determine if an ID exists in the database
    length = 7,  # Base length (automatically increases if a collision occurs)
    ab = "16",  # Alphabet type (base64url... URL-safe Base64, 16... hexadecimal)
)
id_dic[s_id] = True
print(s_id)
```

## 概要
- 短いIDを自動生成するツールです
- 生成済みIDとの衝突を回避する仕組みを持っています

## 特徴
- 生成されるIDの長さを指定可能（デフォルトは5文字）
- 生成されたIDが既存のIDと衝突する場合、長さが自動的に増える
- IDに使用するアルファベットを指定可能（デフォルトはURLセーフなBase64だが、16進数も指定できる）
- 内部で暗号学的に安全な乱数生成を使用しており、タイムスタンプなどから乱数を推定する攻撃者に対してある程度の保護を提供
- 生成されたIDが既存のIDと衝突しているかどうかを判断する関数をユーザーが定義する必要がある。この関数は、辞書の引当やDBの引き当てなどを処理することが想定されている。

```python
import sys
import slim_id

id_dic = {}

def is_exists(arg_id):
    return (arg_id in id_dic)

# Slim-IDを使用してIDを生成
s_id = slim_id.gen(is_exists)
id_dic[s_id] = True
print(s_id)

# カスタムパラメータを使用してSlim-IDでIDを生成
s_id = slim_id.gen(
    is_exists,  # IDがデータベースに存在するかどうかを判断する関数
    length = 7,  # 基本長（衝突が発生した場合、自動的に長くなります）
    ab = "16",  # アルファベットの種類（base64url... URLセーフな64進数、16... 16進数）
)
id_dic[s_id] = True
print(s_id)
```
