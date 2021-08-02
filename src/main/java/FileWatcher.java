import java.io.IOException;
import java.nio.file.CopyOption;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public abstract class FileWatcher {
    protected Path targetFolder;
    protected Path resultFolder;
    protected CopyOption[] copyOptions;

    public FileWatcher(Path targetFolder, Path resultFolder) {
        copyOptions = new CopyOption[]{StandardCopyOption.REPLACE_EXISTING};
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
