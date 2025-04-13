import praw
from datetime import datetime


class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id, client_secret=client_secret, user_agent=user_agent
        )

    ## 展示帖子内容
    def display_post_info(
        self,
        submission,
        index=None,
        show_comments=True,
        comment_limit=0,
        truncate=200,
    ):
        if index is not None:
            print(f"\n🎯 第 {index} 个帖子")
        print(f"标题：{submission.title}")
        print(f"作者：{submission.author}")
        print(f"创建时间：{datetime.utcfromtimestamp(submission.created_utc)}")
        print(f"得分（upvotes）：{submission.score}")
        print(f"评论数：{submission.num_comments}")
        print(f"内容：{submission.selftext[:truncate]}")
        print(f"链接：{submission.url}")

        if show_comments:
            print("评论：")
            submission.comments.replace_more(limit=comment_limit)
            for comment in submission.comments.list():
                print(f"- {comment.body[:100]}")  # 可改为存入列表等其他方式

    def fetch_top_posts(self, subreddit_name, limit=5, time_filter="day"):
        subreddit = self.reddit.subreddit(subreddit_name)
        return list(subreddit.top(limit=limit, time_filter=time_filter))

    def format_submission_for_analysis(self, submission, comment_limit=30):
        title = submission.title
        selftext = submission.selftext.strip()
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()[:comment_limit]
        comment_texts = [f"{i+1}. {c.body.strip()}" for i, c in enumerate(comments)]

        result = f"""【标题】\n{title}\n\n【正文】\n{selftext}\n\n【评论】\n"""
        result += "\n".join(comment_texts)

        return result

    def fetch_and_format(self, subreddit_name, limit=5, comment_limit=30):
        posts = self.fetch_top_posts(subreddit_name=subreddit_name, limit=limit)
        formatted_list = []
        for idx, post in enumerate(posts, 1):
            formatted = self.format_submission_for_analysis(
                post, comment_limit=comment_limit
            )
            formatted_list.append(formatted)
        return formatted_list
