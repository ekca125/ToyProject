import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public abstract class FileWatcher {
    protected final List<String> ignoreExtList;
    protected Path targetFolder;
    protected Path resultFolder;

    public FileWatcher(Path targetFolder, Path resultFolder, List<String> ignoreExtList) {
        this.ignoreExtList = ignoreExtList;
        try {
            this.targetFolder = targetFolder.toRealPath();
            this.resultFolder = resultFolder.toRealPath();
        } catch (IOException e) {
            this.targetFolder = null;
            this.resultFolder = null;
        }
    }

    abstract public void startWatch();
}
