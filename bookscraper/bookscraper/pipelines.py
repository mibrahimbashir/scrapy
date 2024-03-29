# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()

        for field in field_names:
            if field != "description":
                val = adapter.get(field)
                val = val.strip()

                adapter[field] = val

        for field in ["product_type", "genre"]:
            val = adapter.get(field)
            val = val.lower()

            adapter[field] = val

        for field in ["price_excl_tax", "price_incl_tax", "tax", "price"]:
            val = adapter.get(field)
            val = float(val[1:])

            adapter[field] = val

        quantity = adapter.get("availability")
        quantity = int(quantity.split("(")[1].split(" ")[0])

        adapter["availability"] = quantity

        reviews = adapter.get("reviews")

        adapter["reviews"] = int(reviews)

        stars = adapter.get("stars")
        stars = stars.split(" ")[1]

        if stars == "Zero":
            adapter["stars"] = 0

        elif stars == "One":
            adapter["stars"] = 1

        elif stars == "Two":
            adapter["stars"] = 2

        elif stars == "Three":
            adapter["stars"] = 3

        elif stars == "Four":
            adapter["stars"] = 4

        elif stars == "Five":
            adapter["stars"] = 5

        return item
