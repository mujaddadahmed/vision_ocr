import io
import os
import base64
import httpx
import logging
import sys
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
import json

# ── Logging Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),          # terminal
        logging.FileHandler("vision_code.log", encoding="utf-8"),  # file
    ]
)
logger = logging.getLogger("vision_code")

app = FastAPI(title="Vision-Code Practice")

# ── Coding Questions Data ─────────────────────────────────────────────────────

QUESTIONS = [
    {
        "id": 1,
        "title": "Two Sum",
        "difficulty": "Easy",
        "tags": ["Array", "Hash Table"],
        "acceptance": "49.5%",
        "description": """Given an array of integers <code>nums</code> and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.

You may assume that each input would have <strong>exactly one solution</strong>, and you may not use the same element twice.

You can return the answer in any order.""",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": ""},
            {"input": "nums = [3,3], target = 6", "output": "[0,1]", "explanation": ""},
        ],
        "constraints": [
            "2 <= nums.length <= 10<sup>4</sup>",
            "-10<sup>9</sup> <= nums[i] <= 10<sup>9</sup>",
            "-10<sup>9</sup> <= target <= 10<sup>9</sup>",
            "Only one valid answer exists."
        ],
        "starter": {
            "python": "def twoSum(self, nums: List[int], target: int) -> List[int]:\n    # Write your solution here\n    pass",
            "javascript": "var twoSum = function(nums, target) {\n    // Write your solution here\n};",
            "java": "public int[] twoSum(int[] nums, int target) {\n    // Write your solution here\n    return new int[]{};\n}",
            "cpp": "vector<int> twoSum(vector<int>& nums, int target) {\n    // Write your solution here\n    return {};\n}"
        }
    },
    {
        "id": 2,
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "tags": ["String", "Stack"],
        "acceptance": "40.1%",
        "description": """Given a string <code>s</code> containing just the characters <code>'('</code>, <code>')'</code>, <code>'{'</code>, <code>'}'</code>, <code>'['</code> and <code>']'</code>, determine if the input string is valid.

An input string is valid if:
<ul>
<li>Open brackets must be closed by the same type of brackets.</li>
<li>Open brackets must be closed in the correct order.</li>
<li>Every close bracket has a corresponding open bracket of the same type.</li>
</ul>""",
        "examples": [
            {"input": 's = "()"', "output": "true", "explanation": ""},
            {"input": 's = "()[]{}"', "output": "true", "explanation": ""},
            {"input": 's = "(]"', "output": "false", "explanation": ""},
        ],
        "constraints": [
            "1 <= s.length <= 10<sup>4</sup>",
            "s consists of parentheses only '()[]{}'."
        ],
        "starter": {
            "python": "def isValid(self, s: str) -> bool:\n    # Write your solution here\n    pass",
            "javascript": "var isValid = function(s) {\n    // Write your solution here\n};",
            "java": "public boolean isValid(String s) {\n    // Write your solution here\n    return false;\n}",
            "cpp": "bool isValid(string s) {\n    // Write your solution here\n    return false;\n}"
        }
    },
    {
        "id": 3,
        "title": "Merge Two Sorted Lists",
        "difficulty": "Easy",
        "tags": ["Linked List", "Recursion"],
        "acceptance": "62.3%",
        "description": """You are given the heads of two sorted linked lists <code>list1</code> and <code>list2</code>.

Merge the two lists into one <strong>sorted</strong> list. The list should be made by splicing together the nodes of the first two lists.

Return <em>the head of the merged linked list</em>.""",
        "examples": [
            {"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]", "explanation": ""},
            {"input": "list1 = [], list2 = []", "output": "[]", "explanation": ""},
            {"input": "list1 = [], list2 = [0]", "output": "[0]", "explanation": ""},
        ],
        "constraints": [
            "The number of nodes in both lists is in the range [0, 50].",
            "-100 <= Node.val <= 100",
            "Both list1 and list2 are sorted in non-decreasing order."
        ],
        "starter": {
            "python": "def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:\n    # Write your solution here\n    pass",
            "javascript": "var mergeTwoLists = function(list1, list2) {\n    // Write your solution here\n};",
            "java": "public ListNode mergeTwoLists(ListNode list1, ListNode list2) {\n    // Write your solution here\n    return null;\n}",
            "cpp": "ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {\n    // Write your solution here\n    return nullptr;\n}"
        }
    },
    {
        "id": 4,
        "title": "Maximum Subarray",
        "difficulty": "Medium",
        "tags": ["Array", "Divide and Conquer", "Dynamic Programming"],
        "acceptance": "50.7%",
        "description": """Given an integer array <code>nums</code>, find the <strong>subarray</strong> with the largest sum, and return <em>its sum</em>.

A <strong>subarray</strong> is a contiguous non-empty sequence of elements within an array.""",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "The subarray [4,-1,2,1] has the largest sum 6."},
            {"input": "nums = [1]", "output": "1", "explanation": "The subarray [1] has the largest sum 1."},
            {"input": "nums = [5,4,-1,7,8]", "output": "23", "explanation": "The subarray [5,4,-1,7,8] has the largest sum 23."},
        ],
        "constraints": [
            "1 <= nums.length <= 10<sup>5</sup>",
            "-10<sup>4</sup> <= nums[i] <= 10<sup>4</sup>"
        ],
        "starter": {
            "python": "def maxSubArray(self, nums: List[int]) -> int:\n    # Write your solution here\n    pass",
            "javascript": "var maxSubArray = function(nums) {\n    // Write your solution here\n};",
            "java": "public int maxSubArray(int[] nums) {\n    // Write your solution here\n    return 0;\n}",
            "cpp": "int maxSubArray(vector<int>& nums) {\n    // Write your solution here\n    return 0;\n}"
        }
    },
    {
        "id": 5,
        "title": "Binary Search",
        "difficulty": "Easy",
        "tags": ["Array", "Binary Search"],
        "acceptance": "55.1%",
        "description": """Given an array of integers <code>nums</code> which is sorted in ascending order, and an integer <code>target</code>, write a function to search <code>target</code> in <code>nums</code>. If <code>target</code> exists, then return its index. Otherwise, return <code>-1</code>.

You must write an algorithm with <code>O(log n)</code> runtime complexity.""",
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4", "explanation": "9 exists in nums and its index is 4."},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1", "explanation": "2 does not exist in nums so return -1."},
        ],
        "constraints": [
            "1 <= nums.length <= 10<sup>4</sup>",
            "-10<sup>4</sup> < nums[i], target < 10<sup>4</sup>",
            "All the integers in nums are unique.",
            "nums is sorted in ascending order."
        ],
        "starter": {
            "python": "def search(self, nums: List[int], target: int) -> int:\n    # Write your solution here\n    pass",
            "javascript": "var search = function(nums, target) {\n    // Write your solution here\n};",
            "java": "public int search(int[] nums, int target) {\n    // Write your solution here\n    return -1;\n}",
            "cpp": "int search(vector<int>& nums, int target) {\n    // Write your solution here\n    return -1;\n}"
        }
    },
    {
        "id": 6,
        "title": "Climbing Stairs",
        "difficulty": "Easy",
        "tags": ["Math", "Dynamic Programming", "Memoization"],
        "acceptance": "52.2%",
        "description": """You are climbing a staircase. It takes <code>n</code> steps to reach the top.

Each time you can either climb <code>1</code> or <code>2</code> steps. In how many distinct ways can you climb to the top?""",
        "examples": [
            {"input": "n = 2", "output": "2", "explanation": "There are two ways to climb to the top. 1. 1 step + 1 step  2. 2 steps"},
            {"input": "n = 3", "output": "3", "explanation": "There are three ways to climb to the top. 1. 1 step + 1 step + 1 step  2. 1 step + 2 steps  3. 2 steps + 1 step"},
        ],
        "constraints": [
            "1 <= n <= 45"
        ],
        "starter": {
            "python": "def climbStairs(self, n: int) -> int:\n    # Write your solution here\n    pass",
            "javascript": "var climbStairs = function(n) {\n    // Write your solution here\n};",
            "java": "public int climbStairs(int n) {\n    // Write your solution here\n    return 0;\n}",
            "cpp": "int climbStairs(int n) {\n    // Write your solution here\n    return 0;\n}"
        }
    },
    {
        "id": 7,
        "title": "Reverse Linked List",
        "difficulty": "Easy",
        "tags": ["Linked List", "Recursion"],
        "acceptance": "75.0%",
        "description": """Given the <code>head</code> of a singly linked list, reverse the list, and return <em>the reversed list</em>.""",
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]", "explanation": ""},
            {"input": "head = [1,2]", "output": "[2,1]", "explanation": ""},
            {"input": "head = []", "output": "[]", "explanation": ""},
        ],
        "constraints": [
            "The number of nodes in the list is the range [0, 5000].",
            "-5000 <= Node.val <= 5000"
        ],
        "starter": {
            "python": "def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n    # Write your solution here\n    pass",
            "javascript": "var reverseList = function(head) {\n    // Write your solution here\n};",
            "java": "public ListNode reverseList(ListNode head) {\n    // Write your solution here\n    return null;\n}",
            "cpp": "ListNode* reverseList(ListNode* head) {\n    // Write your solution here\n    return nullptr;\n}"
        }
    },
    {
        "id": 8,
        "title": "Number of Islands",
        "difficulty": "Medium",
        "tags": ["Array", "BFS", "DFS", "Matrix", "Union Find"],
        "acceptance": "57.9%",
        "description": """Given an <code>m x n</code> 2D binary grid <code>grid</code> which represents a map of <code>'1'</code>s (land) and <code>'0'</code>s (water), return <em>the number of islands</em>.

An <strong>island</strong> is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.""",
        "examples": [
            {"input": 'grid = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]', "output": "1", "explanation": ""},
            {"input": 'grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]', "output": "3", "explanation": ""},
        ],
        "constraints": [
            "m == grid.length",
            "n == grid[i].length",
            "1 <= m, n <= 300",
            "grid[i][j] is '0' or '1'."
        ],
        "starter": {
            "python": "def numIslands(self, grid: List[List[str]]) -> int:\n    # Write your solution here\n    pass",
            "javascript": "var numIslands = function(grid) {\n    // Write your solution here\n};",
            "java": "public int numIslands(char[][] grid) {\n    // Write your solution here\n    return 0;\n}",
            "cpp": "int numIslands(vector<vector<char>>& grid) {\n    // Write your solution here\n    return 0;\n}"
        }
    },
    {
        "id": 9,
        "title": "LRU Cache",
        "difficulty": "Medium",
        "tags": ["Hash Table", "Linked List", "Design", "Doubly-Linked List"],
        "acceptance": "42.3%",
        "description": """Design a data structure that follows the constraints of a <strong>Least Recently Used (LRU) cache</strong>.

Implement the <code>LRUCache</code> class:
<ul>
<li><code>LRUCache(int capacity)</code> Initialize the LRU cache with <strong>positive</strong> size <code>capacity</code>.</li>
<li><code>int get(int key)</code> Return the value of the <code>key</code> if the key exists, otherwise return <code>-1</code>.</li>
<li><code>void put(int key, int value)</code> Update the value of the <code>key</code> if the <code>key</code> exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the <code>capacity</code> from this operation, <strong>evict</strong> the least recently used key.</li>
</ul>
The functions <code>get</code> and <code>put</code> must each run in <code>O(1)</code> average time complexity.""",
        "examples": [
            {"input": '["LRUCache","put","put","get","put","get","put","get","get","get"]\n[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]', "output": "[null,null,null,1,null,-1,null,-1,3,4]", "explanation": ""},
        ],
        "constraints": [
            "1 <= capacity <= 3000",
            "0 <= key <= 10<sup>4</sup>",
            "0 <= value <= 10<sup>5</sup>",
            "At most 2 * 10<sup>5</sup> calls will be made to get and put."
        ],
        "starter": {
            "python": "class LRUCache:\n    def __init__(self, capacity: int):\n        # Initialize here\n        pass\n\n    def get(self, key: int) -> int:\n        # Write your solution here\n        pass\n\n    def put(self, key: int, value: int) -> None:\n        # Write your solution here\n        pass",
            "javascript": "class LRUCache {\n    constructor(capacity) {\n        // Initialize here\n    }\n    get(key) {\n        // Write your solution here\n    }\n    put(key, value) {\n        // Write your solution here\n    }\n}",
            "java": "class LRUCache {\n    public LRUCache(int capacity) {\n        // Initialize here\n    }\n    public int get(int key) {\n        return -1;\n    }\n    public void put(int key, int value) {\n        // Write your solution here\n    }\n}",
            "cpp": "class LRUCache {\npublic:\n    LRUCache(int capacity) {\n        // Initialize here\n    }\n    int get(int key) {\n        return -1;\n    }\n    void put(int key, int value) {\n        // Write your solution here\n    }\n};"
        }
    },
    {
        "id": 10,
        "title": "Word Search",
        "difficulty": "Medium",
        "tags": ["Array", "Backtracking", "Matrix"],
        "acceptance": "40.2%",
        "description": """Given an <code>m x n</code> grid of characters <code>board</code> and a string <code>word</code>, return <em><code>true</code> if <code>word</code> exists in the grid</em>.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.""",
        "examples": [
            {"input": 'board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"', "output": "true", "explanation": ""},
            {"input": 'board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"', "output": "true", "explanation": ""},
            {"input": 'board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"', "output": "false", "explanation": ""},
        ],
        "constraints": [
            "m == board.length",
            "n = board[i].length",
            "1 <= m, n <= 6",
            "1 <= word.length <= 15",
            "board and word consists of only lowercase and uppercase English letters."
        ],
        "starter": {
            "python": "def exist(self, board: List[List[str]], word: str) -> bool:\n    # Write your solution here\n    pass",
            "javascript": "var exist = function(board, word) {\n    // Write your solution here\n};",
            "java": "public boolean exist(char[][] board, String word) {\n    // Write your solution here\n    return false;\n}",
            "cpp": "bool exist(vector<vector<char>>& board, string word) {\n    // Write your solution here\n    return false;\n}"
        }
    }
]

# ── API Routes ────────────────────────────────────────────────────────────────

@app.get("/api/questions")
async def get_questions():
    summary = []
    for q in QUESTIONS:
        summary.append({
            "id": q["id"],
            "title": q["title"],
            "difficulty": q["difficulty"],
            "tags": q["tags"],
            "acceptance": q["acceptance"]
        })
    return summary


@app.get("/api/questions/{question_id}")
async def get_question(question_id: int):
    for q in QUESTIONS:
        if q["id"] == question_id:
            return q
    raise HTTPException(status_code=404, detail="Question not found")


@app.post("/api/extract-code")
async def extract_code(file: UploadFile = File(...)):
    request_id = f"req-{int(time.time()*1000)}"
    logger.info(f"[{request_id}] ── /api/extract-code called ──────────────────────")

    # ── API key check ──────────────────────────────────────────────────────────
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        logger.error(f"[{request_id}] GROQ_API_KEY is not set in environment variables")
        raise HTTPException(status_code=500, detail="Service configuration error")
    logger.debug(f"[{request_id}] API key present — prefix: {api_key[:6]}***{api_key[-3:]}")

    # ── File validation ────────────────────────────────────────────────────────
    contents = await file.read()
    file_size_kb = len(contents) / 1024
    logger.info(f"[{request_id}] File received — name: '{file.filename}', "
                f"content-type: '{file.content_type}', size: {file_size_kb:.1f} KB")

    if len(contents) > 10 * 1024 * 1024:
        logger.warning(f"[{request_id}] File too large ({file_size_kb:.0f} KB) — rejected")
        raise HTTPException(status_code=400, detail="Image too large. Please use an image under 10MB.")

    mime = file.content_type or "image/jpeg"
    if mime not in ("image/jpeg", "image/png", "image/webp", "image/gif"):
        logger.warning(f"[{request_id}] Unrecognised mime type '{mime}' — falling back to image/jpeg")
        mime = "image/jpeg"

    # ── Resize image to keep payload small (max 1024px on longest side) ────────
    MAX_PX = 1024
    try:
        img = Image.open(io.BytesIO(contents))
        if max(img.size) > MAX_PX:
            img.thumbnail((MAX_PX, MAX_PX), Image.LANCZOS)
            logger.debug(f"[{request_id}] Resized image to {img.size}")
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=85)
        contents = buf.getvalue()
        mime = "image/jpeg"
        logger.debug(f"[{request_id}] Image after resize — size: {len(contents)/1024:.1f} KB")
    except Exception as img_err:
        logger.warning(f"[{request_id}] Could not resize image ({img_err}), sending as-is")

    b64_image = base64.b64encode(contents).decode("utf-8")
    logger.debug(f"[{request_id}] Base64 encoded — length: {len(b64_image)} chars")

    # ── Build payload ──────────────────────────────────────────────────────────
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime};base64,{b64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": (
                            "Extract only the source code visible in this image. "
                            "Preserve the exact indentation, spacing, line breaks, and formatting as written. "
                            "Do NOT correct any syntax errors, variable names, or logic — transcribe exactly what is written. "
                            "Output ONLY the raw code with no explanation, no markdown fences, no commentary."
                        )
                    }
                ]
            }
        ],
        "max_tokens": 2048,
        "temperature": 0
    }
    logger.debug(f"[{request_id}] Payload built — model: '{payload['model']}', "
                 f"max_tokens: {payload['max_tokens']}, temperature: {payload['temperature']}")

    # ── HTTP request ───────────────────────────────────────────────────────────
    target_url = "https://api.groq.com/openai/v1/chat/completions"
    logger.info(f"[{request_id}] Sending POST → {target_url}")
    t_start = time.monotonic()

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                target_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                json=payload
            )

        elapsed_ms = (time.monotonic() - t_start) * 1000
        logger.info(f"[{request_id}] Response received — HTTP {response.status_code} in {elapsed_ms:.0f} ms")
        logger.debug(f"[{request_id}] Response headers: {dict(response.headers)}")

        # ── Non-200 handling ───────────────────────────────────────────────────
        if response.status_code != 200:
            raw_body = response.text
            logger.error(f"[{request_id}] Non-200 status {response.status_code}. "
                         f"Response body: {raw_body[:500]}")
            raise HTTPException(status_code=502, detail="Could not process the image. Please try again.")

        # ── Parse response ─────────────────────────────────────────────────────
        try:
            data = response.json()
        except Exception as parse_err:
            logger.error(f"[{request_id}] Failed to parse JSON response: {parse_err}. "
                         f"Raw body: {response.text[:300]}")
            raise HTTPException(status_code=502, detail="Could not process the image. Please try again.")

        logger.debug(f"[{request_id}] Parsed response JSON — keys: {list(data.keys())}")

        # ── Validate response structure ────────────────────────────────────────
        if "error" in data:
            err = data["error"]
            logger.error(f"[{request_id}] API returned error object — "
                         f"code: {err.get('code')}, message: {err.get('message')}, "
                         f"type: {err.get('type')}")
            raise HTTPException(status_code=502, detail="Could not process the image. Please try again.")

        if not data.get("choices"):
            logger.error(f"[{request_id}] Response has no 'choices'. Full response: {json.dumps(data)[:400]}")
            raise HTTPException(status_code=502, detail="Could not process the image. Please try again.")

        choice = data["choices"][0]
        finish_reason = choice.get("finish_reason")
        logger.info(f"[{request_id}] Choice[0] finish_reason: '{finish_reason}'")

        if finish_reason not in ("stop", None):
            logger.warning(f"[{request_id}] Unexpected finish_reason: '{finish_reason}'")

        raw_code = choice.get("message", {}).get("content", "")
        logger.info(f"[{request_id}] Raw content length: {len(raw_code)} chars")
        logger.debug(f"[{request_id}] Raw content preview: {repr(raw_code[:200])}")

        # ── Strip markdown fences if model added them ──────────────────────────
        code = raw_code.strip()
        if code.startswith("```"):
            logger.debug(f"[{request_id}] Stripping markdown code fences from response")
            lines = code.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            code = "\n".join(lines)

        if not code.strip():
            logger.warning(f"[{request_id}] Extracted code is empty after stripping")
        else:
            logger.info(f"[{request_id}] ✓ Code extracted successfully — {len(code)} chars, "
                        f"{code.count(chr(10))+1} lines")

        # ── Usage stats ────────────────────────────────────────────────────────
        usage = data.get("usage", {})
        if usage:
            logger.info(f"[{request_id}] Token usage — prompt: {usage.get('prompt_tokens')}, "
                        f"completion: {usage.get('completion_tokens')}, "
                        f"total: {usage.get('total_tokens')}")

        return {"code": code}

    except HTTPException:
        raise  # re-raise our own HTTPExceptions unchanged

    except httpx.TimeoutException as te:
        elapsed_ms = (time.monotonic() - t_start) * 1000
        logger.error(f"[{request_id}] Request timed out after {elapsed_ms:.0f} ms — {te}")
        raise HTTPException(status_code=504, detail="Request timed out. Please try again.")

    except httpx.ConnectError as ce:
        logger.error(f"[{request_id}] Connection error — could not reach API endpoint: {ce}")
        raise HTTPException(status_code=502, detail="Could not process the image. Please try again.")

    except httpx.HTTPStatusError as se:
        logger.error(f"[{request_id}] HTTP status error: {se}")
        raise HTTPException(status_code=502, detail="Could not process the image. Please try again.")

    except Exception as e:
        logger.exception(f"[{request_id}] Unexpected exception in extract_code: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred processing your image.")


# ── Startup Event ────────────────────────────────────────────────────────────
@app.on_event("startup")
async def on_startup():
    key = os.environ.get("GROQ_API_KEY", "")
    if key:
        logger.info(f"Startup — GROQ_API_KEY loaded (prefix: {key[:6]}***)")
    else:
        logger.critical("Startup — GROQ_API_KEY is NOT set! /api/extract-code will fail.")

# ── Static Files & SPA ────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("static/index.html")

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(full_path: str):
    return FileResponse("static/index.html")
