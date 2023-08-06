
# 短いIDの生成ツール [slim_id]

import sys
import secrets	# 暗号学的乱数生成装置 (ハードウエアエントロピー等を用いて予測不可能にしてある)
from sout import sout

# アルファベット一覧辞書
ab_dic = {
	"16": "0123456789abcdef",
	"base64url": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_",
}

# ID生成 [slim_id]
def gen(
	is_exists,	# 既存のDBに存在するかを判定する関数
	length = 5,	# 基本長 (衝突時には自動的に長くなる)
	ab = "base64url",	# アルファベットの種類 (base64url...urlセーフな64進数, 16...16進)
):
	if length > 65536: raise Exception("[slim-id error] The maximum length of an ID that can be generated with slim-id is 65536.")
	seq_ls = [secrets.choice(ab_dic[ab])
		for _ in range(length)]
	ret_id = "".join(seq_ls)
	# 衝突時はlengthを長くする
	if is_exists(ret_id) is True:
		return gen(is_exists, length + 1, ab)
	return ret_id
