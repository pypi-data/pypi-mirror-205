from interpret.blackbox import MorrisSensitivity
from sklearn.pipeline import Pipeline

from explainability.structured.core.structured_explainer import Path, \
    SKExplainer
from explainability.structured.core.structured_manipulator import \
    StructuredManipulator


class MorrisExplainer(SKExplainer):
    """
    Uses Morris sensitivity global explanations to explain challenges.
    """

    def explain_global(self, trained_model: Pipeline,
                       sm: StructuredManipulator,
                       path: Path) -> None:
        preprocessor = trained_model.named_steps["preprocessor"]

        x, _, _, _ = sm.train_test_split()

        x = preprocessor.transform(x)
        feature_names = preprocessor.get_feature_names_out()

        msa = MorrisSensitivity(trained_model.named_steps["model"],
                                x,
                                feature_names=feature_names)
        g = msa.explain_global()
        fig = g.visualize()
        fig.write_image(str(path), format="png")
