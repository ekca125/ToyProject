import java.io.IOException;
import java.nio.file.CopyOption;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.List;

public abstract class FileWatcher {
    protected Path targetFolder;
    protected Path resultFolder;
    protected final List<String> ignoreExtList;

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
