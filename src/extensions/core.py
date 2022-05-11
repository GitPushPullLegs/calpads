from src.extensions import BaseAPIExt


class Core(BaseAPIExt):
    def get_leas(self):
        return self.api.get_resource("LEAS?format=JSON")

    def get_schools(self, lea_code: str):
        return self.api.get_resource(f"/SchoolListingAll?lea={lea_code}&format=JSON")
