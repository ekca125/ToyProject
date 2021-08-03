import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class JDownloaderScheduleMover extends FileScheduleWatcher {
    public JDownloaderScheduleMover(Path targetFolder, Path resultFolder, List<String> ignoreExtList) {
        super(targetFolder, resultFolder, ignoreExtList);
    }

    public static void main(String[] args) {
        try {
            Path targetFolder = Paths.get(args[0]);
            Path resultFolder = Paths.get(args[1]);
            //리스트 추가
            List<String> ignoreExtList = List.of(".part", ".encrypt");

            JDownloaderScheduleMover jDownloaderScheduleMover = new JDownloaderScheduleMover(targetFolder, resultFolder, ignoreExtList);
            jDownloaderScheduleMover.startWatch();
        } catch (ArrayIndexOutOfBoundsException arrayIndexOutOfBoundsException) {
            System.out.println("Not Enough Values");
        }
    }
}
