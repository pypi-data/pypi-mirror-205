from google.protobuf.empty_pb2 import Empty

from featurestore.core.entities.feature_set_popularity import FeatureSetPopularity
from featurestore.core.entities.recently_used_feature_set import RecentlyUsedFeatureSet
from featurestore.core.entities.recently_used_project import RecentlyUsedProject


class Dashboard:
    def __init__(self, stub):
        self._stub = stub

    def get_feature_sets_popularity(self):
        """Get popular feature sets.

        Returns:
            List of feature sets popularity

        Typical example:
            fs_popularity = client.dashboard.get_feature_sets_popularity()
        """
        response = self._stub.GetFeatureSetsPopularity(Empty())
        return [FeatureSetPopularity(self._stub, popular_feature_set) for popular_feature_set in response.feature_sets]

    def get_recently_used_projects(self):
        """Get projects that were recently utilized.

        Returns:
            List of references to projects

        Typical example:
            recently_used_projects = client.dashboard.get_recently_used_projects()
        """
        response = self._stub.GetRecentlyUsedProjects(Empty())
        return [RecentlyUsedProject(self._stub, project) for project in response.projects]

    def get_recently_used_feature_sets(self):
        """Get feature sets that were recently utilized.

        Returns:
            List of references to feature sets

        Typical example:
            recently_used_feature_sets = client.dashboard.get_recently_used_feature_sets()
        """
        response = self._stub.GetRecentlyUsedFeatureSets(Empty())
        return [RecentlyUsedFeatureSet(self._stub, feature_set) for feature_set in response.feature_sets]
