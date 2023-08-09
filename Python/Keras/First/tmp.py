class Solution:
    def isPalindrome(self, x: int) -> bool:
        s = str(x)
        min = 0
        max = len(s)-1
        while min < max:
            if s[min] != s[max]:
                return False
            min += 1
            max -= 1
        return True

sol = Solution()
res = sol.isPalindrome(121)

print(res)

x = 10

print(x % 10)