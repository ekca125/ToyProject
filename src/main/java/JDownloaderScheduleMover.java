import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class JDownloaderScheduleMover extends FileScheduleWatcher {
    public JDownloaderScheduleMover(Path targetFolder, Path resultFolder, List<String> ignoreExtList) {
        super(targetFolder, resultFolder, ignoreExtList);
    }

    public JDownloaderScheduleMover(Path targetFolder, Path resultFolder, List<String> ignoreExtList, int delayHour) {
        super(targetFolder, resultFolder, ignoreExtList, delayHour);
    }

    public static void main(String[] args) {
        try {
            Path targetFolder = Paths.get(args[0]);
            Path resultFolder = Paths.get(args[1]);
            int delayHour = Integer.parseInt(args[2]);
            List<String> ignoreExtList = List.of(".part", ".encrypt");

            JDownloaderScheduleMover jDownloaderScheduleMover = new JDownloaderScheduleMover(targetFolder, resultFolder, ignoreExtList, delayHour);
            jDownloaderScheduleMover.startWatch();
        } catch (ArrayIndexOutOfBoundsException arrayIndexOutOfBoundsException) {
            System.out.println("대상 폴더 또는 결과 폴더, 지연시간이 지정되지 않았습니다. args[0] = 대상폴더 args[1] = 결과 폴더 args[2] = 대기시간");
        }
    }
}
