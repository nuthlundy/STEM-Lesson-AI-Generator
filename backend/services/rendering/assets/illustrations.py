class IllustrationLibrary:
    @staticmethod
    def get_illustration(topic: str) -> str:
        illustrations = {
            "math": "geometry_vector.png",
            "science": "microscope_vector.png",
            "technology": "robotics_arm_vector.png",
            "engineering": "blueprint_bridge_vector.png"
        }
        return illustrations.get(topic.lower(), "generic_science_vector.png")
