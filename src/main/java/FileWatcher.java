import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.List;

public abstract class FileWatcher {
    protected Path targetFolder;
    protected Path resultFolder;
    protected CopyOption[] copyOptions;

    public FileWatcher(Path targetFolder,Path resultFolder){
        copyOptions = new CopyOption[]{StandardCopyOption.REPLACE_EXISTING};
        try {
            this.targetFolder = targetFolder.toRealPath();
            this.resultFolder = resultFolder.toRealPath();
        }
        catch (IOException e) {
            this.targetFolder = null;
            this.resultFolder = null;
        }
    }

    final public void moveFile(Path fileName){
        Path filePath = Paths.get(this.targetFolder.toString(),fileName.toString());
        Path resultFilePath = Paths.get(this.resultFolder.toString(),fileName.toString());

        try {
            BasicFileAttributes basicFileAttributes = Files.readAttributes(filePath, BasicFileAttributes.class);
            if((!fileName.toString().contains(".part"))
                    && (!fileName.toString().contains(".encrypted"))
                    && (!basicFileAttributes.isDirectory())){
                Files.move(filePath,resultFilePath,copyOptions);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    abstract public void startWatch();
}
