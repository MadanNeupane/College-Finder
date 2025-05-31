import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from universities.models import University
from blogs.models import Post
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Command(BaseCommand):
    help = "Populates universities and blog posts from fixtures (ignoring tags)"

    def handle(self, *args, **kwargs):
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

                # Handle required fields that may be missing
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

            self.stdout.write(self.style.SUCCESS("✅ Universities loaded successfully."))
        except Exception as e:
            self.stderr.write(f"❌ Error loading universities: {e}")

        # --- Blog Posts ---
        try:
            with open(os.path.join(base_dir, "blogs.json"), "r", encoding="utf-8") as f:
                blog_data = json.load(f)

            Post.objects.all().delete()

            for item in blog_data:
                if item.get("model") != "blogs.post":
                    continue
                fields = item["fields"]

                fields.pop("tags", None)  # skip tags
                fields.pop("author", None)  # remove author key to avoid conflict

                author = User.objects.filter(id=2).first()
                if not author:
                    raise Exception("User with ID 2 not found. Create it before running this.")

                Post.objects.create(
                    id=item["pk"],
                    author=author,
                    **fields
                )

            self.stdout.write(self.style.SUCCESS("✅ Blog posts loaded successfully (tags skipped)."))
        except Exception as e:
            self.stderr.write(f"❌ Error loading blog posts: {e}")
