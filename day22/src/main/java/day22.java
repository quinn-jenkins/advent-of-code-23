import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.concurrent.LinkedBlockingQueue;

public class day22
{
    private static final Logger logger = LoggerFactory.getLogger(day22.class);

    public static void main(String[] args)
    {
        new day22();
    }

    public day22()
    {
        try
        {
            List<String> allLines = Files.readAllLines(Paths.get("src/main/resources/input.txt"));
            playJenga(allLines);
        } catch (Exception e)
        {
            logger.error("Caught exception", e);
        }
    }

    private void playJenga(List<String> puzzle)
    {
        List<Brick> bricks = new ArrayList<>();
        Map<Integer, List<Brick>> bricksByLayer = new TreeMap<>();
        int maxX = 0;
        int maxY = 0;
        int brickId = 0;
        for (String brickString : puzzle)
        {
            String[] parts = brickString.split("~");
            Integer[] startCoords = convertToInts(parts[0].split(","));
            Integer[] endCoords = convertToInts(parts[1].split(","));
            GridCoord start = new GridCoord(startCoords[0], startCoords[1], startCoords[2]);
            GridCoord end = new GridCoord(endCoords[0], endCoords[1], endCoords[2]);
            Brick brick = new Brick(brickId, start, end);
            bricks.add(brick);
            int zStart = start.z();
            int zEnd = end.z();
            for (int z = zStart; z <= zEnd; z++)
            {
                bricksByLayer.computeIfAbsent(z, k -> new ArrayList<>()).add(brick);
            }
            // Assumes that the end is always either the same as the start x/y or larger
            maxX = Math.max(end.x(), maxX);
            maxY = Math.max(end.y(), maxY);
            brickId++;
        }

        // TODO: I'm sure that this can all be done in one step by keeping track of the brick at the highest point in an
        //  x-y coordinate when doing the falling simulation
        Map<Integer, List<Brick>> fallenBricks = completeFallingBricks(bricks, maxX, maxY);
        Map<Integer, List<Integer>> supportingBricks = findBricksThatSupportOtherBricks(bricks, fallenBricks);

        Map<Integer, List<Integer>> supportedByMap = invertMap(supportingBricks);
        Set<Integer> freeBricks = new TreeSet<>();
        Set<Integer> bricksSupportingOthers = new TreeSet<>();
        for (Map.Entry<Integer, List<Integer>> entry : supportingBricks.entrySet())
        {
            if (entry.getValue().isEmpty())
            {
                freeBricks.add(entry.getKey());
            }
            boolean allSupportedMoreThanOnce = true;
            for (Integer supportedBrick : entry.getValue())
            {
                if (supportedByMap.get(supportedBrick).size() <= 1)
                {
                    allSupportedMoreThanOnce = false;
                    break;
                }
            }
            if (allSupportedMoreThanOnce)
            {
                freeBricks.add(entry.getKey());
            } else
            {
                bricksSupportingOthers.add(entry.getKey());
            }
        }

        logger.info("Part One: {}", freeBricks.size());

        int sum = 0;
        for (Integer brick : bricksSupportingOthers)
        {
            int chainReactionSize = getChainReactionSize(brick, supportingBricks, supportedByMap);
            sum += chainReactionSize;
        }

        logger.info("Part Two: {}", sum);

    }

    /**
     * @param bricks       All bricks in the input
     * @param fallenBricks Map of Layer # (Z-coord) to the list of bricks that exist in that layer
     * @return a map of Brick (Key) -> List of all bricks that the Key brick is supporting
     */
    private Map<Integer, List<Integer>> findBricksThatSupportOtherBricks(List<Brick> bricks, Map<Integer, List<Brick>> fallenBricks)
    {
        List<Brick> layerBelow = null;
        Map<Integer, List<Integer>> supportingBricks = new TreeMap<>();
        for (Brick b : bricks)
        {
            supportingBricks.put(b.getBrickId(), new ArrayList<>());
        }
        for (Map.Entry<Integer, List<Brick>> entry : fallenBricks.entrySet())
        {
            if (layerBelow == null)
            {
                layerBelow = entry.getValue();
                continue;
            }

            for (Brick possibleSuppportingBrick : layerBelow)
            {
                for (Brick brick : entry.getValue())
                {
                    if (possibleSuppportingBrick.supportsOtherBrick(brick))
                    {
                        supportingBricks.get(possibleSuppportingBrick.getBrickId()).add(brick.getBrickId());
                    }
                }
            }

            layerBelow = entry.getValue();
        }
        return supportingBricks;
    }

    /**
     * Supporting Bricks: Key is supporting each of the bricks in the value list
     * Bricks Supported By: Key is supported by each of the bricks in the value list
     */
    private int getChainReactionSize(Integer brick, Map<Integer, List<Integer>> supportingBricks, Map<Integer, List<Integer>> bricksSupportedBy)
    {
        int numDisintegrated = 0;
        Set<Integer> disintegratedBricks = new HashSet<>();
        Queue<Integer> brickQueue = new LinkedBlockingQueue<>();
        brickQueue.add(brick);

        while (!brickQueue.isEmpty())
        {
            Integer currentBrick = brickQueue.poll();
            disintegratedBricks.add(currentBrick);
            for (Integer supportedBrick : supportingBricks.get(currentBrick))
            {
                List<Integer> bricksHoldingThisBrick = new ArrayList<>(bricksSupportedBy.get(supportedBrick));
                bricksHoldingThisBrick.removeAll(disintegratedBricks);
                if (bricksHoldingThisBrick.isEmpty())
                {
                    numDisintegrated++;
                    brickQueue.add(supportedBrick);
                }
            }
        }
        return numDisintegrated;
    }

    /**
     * Computes the inverse of the original map such that each value in the original map links back to the list of keys that originally pointed to it
     *
     * @param orig Original map of Brick -> All bricks being supported by the Key brick
     * @return Inverse map which is now Brick -> All bricks that support the key brick
     */
    private Map<Integer, List<Integer>> invertMap(Map<Integer, List<Integer>> orig)
    {
        Map<Integer, List<Integer>> inverted = new TreeMap<>();
        for (Map.Entry<Integer, List<Integer>> entry : orig.entrySet())
        {
            for (Integer s : entry.getValue())
            {
                inverted.computeIfAbsent(s, k -> new ArrayList<>()).add(entry.getKey());
            }
        }
        return inverted;
    }

    /**
     * Completes the falling simulation and returns a map of Layer -> List of all the bricks that exist in that layer
     *
     * @param allBricks All bricks from the input file
     * @param widthX    Width of the grid in the X domain
     * @param widthY    Width of the grid in the Y domain
     * @return Map of Layer # (Z coordinate) -> List of all bricks that exist in that layer. Note that in the case of a vertical brick,
     * a brick can appear in multiple layers
     */
    private Map<Integer, List<Brick>> completeFallingBricks(List<Brick> allBricks, int widthX, int widthY)
    {
        Map<Integer, List<Brick>> fallenBricks = new TreeMap<>();
        int[][] highestBrickAtXY = new int[widthX + 1][widthY + 1];
        allBricks = allBricks.stream()
                .sorted(Comparator.comparingInt(Brick::getMaxZ))
                .toList();
        for (Brick b : allBricks)
        {
            int highestSupport = 0;
            for (GridCoord gridCoord : b.getBrickSpan())
            {
                highestSupport = Math.max(highestBrickAtXY[gridCoord.x()][gridCoord.y()], highestSupport);
            }
            int brickSettledLayer = highestSupport + 1;
            Brick newBrick = b.shiftBrickDown(brickSettledLayer);
            for (int layer = brickSettledLayer; layer <= brickSettledLayer + newBrick.getDeltaZ(); layer++)
            {
                fallenBricks.computeIfAbsent(layer, k -> new ArrayList<>()).add(newBrick);
            }
            // we're supported, so see if we update the highest point anywhere
            for (GridCoord gridCoord : newBrick.getBrickSpan())
            {
                int currentHighest = highestBrickAtXY[gridCoord.x()][gridCoord.y()];
                if (gridCoord.z() > currentHighest)
                {
                    highestBrickAtXY[gridCoord.x()][gridCoord.y()] = gridCoord.z();
                }
            }
        }

        return fallenBricks;
    }

    private Integer[] convertToInts(String[] numbers)
    {
        Integer[] ints = new Integer[numbers.length];
        for (int i = 0; i < numbers.length; i++)
        {
            int val = Integer.parseInt(numbers[i]);
            ints[i] = val;
        }
        return ints;
    }
}
