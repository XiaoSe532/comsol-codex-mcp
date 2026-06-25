import com.comsol.model.*;
import com.comsol.model.util.*;

public class MinimalModel {
    public static void main(String[] args) {
        ModelUtil.initStandalone(false);
        try {
            Model model = ModelUtil.create("MinimalModel");
            model.component().create("comp1");
            model.component("comp1").geom().create("geom1", 3);
            model.component("comp1").geom("geom1").create("blk1", "Block");
            model.component("comp1").geom("geom1").feature("blk1").set("size", new double[]{1, 1, 1});
            model.component("comp1").geom("geom1").run();
            System.out.println("===MODEL_INFO minimal===");
            System.out.println("domains,boundaries");
            System.out.println(model.component("comp1").geom("geom1").getNDomains() + "," +
                model.component("comp1").geom("geom1").getNBoundaries());
            System.out.flush();
            model.save("MinimalModel.mph");
        } catch (Exception e) {
            System.err.println("FATAL: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        } finally {
            ModelUtil.disconnect();
        }
    }
}

