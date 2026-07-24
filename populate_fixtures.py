# populate_fixtures.py

import os
import json
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college_finder_app.settings")
django.setup()

from universities.models import University
from blogs.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

def main():
    base_dir = os.path.join(settings.BASE_DIR, "fixtures")

    # --- Universities ---
    try:
        with open(os.path.join(base_dir, "universities.json"), "r", encoding="utf-8") as f:
            uni_data = json.load(f)

        University.objects.all().delete()

        for item in uni_data:
            if item.get("model") != "universities.university":
                continue
            fields = item["fields"]

            required_defaults = {
                "scores_overall_rank": 9999,
                "scores_teaching_rank": 9999,
                "scores_research_rank": 9999,
                "scores_citations_rank": 9999,
                "scores_industry_income_rank": 9999,
                "scores_international_outlook_rank": 9999,
            }
            for key, default_val in required_defaults.items():
                if key not in fields or fields[key] is None:
                    fields[key] = default_val

            University.objects.create(id=item["pk"], **fields)

        print("[SUCCESS] Universities loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Error loading universities: {e}")

    # --- Blog Posts ---
    try:
        with open(os.path.join(base_dir, "blogs.json"), "r", encoding="utf-8") as f:
            blog_data = json.load(f)

        Post.objects.all().delete()

        for item in blog_data:
            if item.get("model") != "blogs.post":
                continue
            fields = item["fields"]

            fields.pop("tags", None)
            fields.pop("author", None)

            author = User.objects.filter(id=2).first()
            if not author:
                author = User.objects.first()
            if not author:
                author = User.objects.create_user('author2', 'author2@example.com', 'password123')

            Post.objects.create(
                id=item["pk"],
                author=author,
                **fields
            )

        print("[SUCCESS] Blog posts loaded successfully (tags skipped).")
    except Exception as e:
        print(f"[ERROR] Error loading blog posts: {e}")

if __name__ == "__main__":
    main()
