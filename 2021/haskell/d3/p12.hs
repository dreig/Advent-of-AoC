{- stack script --resolver lts-18.18 -}
import System.Environment ( getArgs )
import Data.List
    ( maximumBy, minimumBy, group, sort, transpose, foldl1', sortBy, groupBy )
import Data.Char ( ord )
import Data.Function (on)
import Control.Applicative (liftA2)


maximumElem :: (Ord a) => [a] -> a
maximumElem = head . maximumBy (compare `on` length) . group . sort

minimumElem :: (Ord a) => [a] -> a
minimumElem = head . minimumBy (compare `on` length) . group . sort

charToInt x | ord' <= 57 && ord' >= 48 = Just (ord' - ord '0')
            | otherwise = Nothing
              where ord' = ord x

fromBinaryString = foldl1' (liftA2 (\acc x -> acc*2 + x)) . map charToInt

solveP1 contents = maybe "something went wrong"
                         show ((*) <$> fromBinaryString mn <*> fromBinaryString mx)
  where
    transposedLines = transpose . lines $ contents
    mn = map minimumElem transposedLines
    mx = map maximumElem transposedLines


solveP2 contents = maybe "something went wrong"
                         show ((*) <$> fromBinaryString mn <*> fromBinaryString mx)
  where
    ls = lines contents
    n = length . head $ ls
    mn = head $ filterByMinority n ls
    mx = head $ filterByMajority n ls

filterByMajority :: Int -> [String] -> [String]
filterByMajority 0 xs = xs
filterByMajority n xs = majorityPrefix n (filterByMajority (n-1) xs)

filterByMinority :: Int -> [String] -> [String]
filterByMinority 0 xs = xs
filterByMinority n xs = minorityPrefix n (filterByMinority (n-1) xs)

majorityPrefix :: Int -> [String] -> [String]
majorityPrefix n xs = maximumBy (compare `on` length) $ partition n xs

minorityPrefix :: Int -> [String] -> [String]
minorityPrefix n xs = minimumBy (compare `on` length) $ partition n xs

partition :: Int -> [String] -> [[String]]
partition n xs = groupBy comparePrefix sortedByPrefix
  where comparePrefix = (==) `on` take n
        sortedByPrefix = sortBy (compare `on` take n) xs

main = do
  args <- getArgs
  contents <- readFile $ head args
  putStrLn $ "P1: " ++ solveP1 contents
  putStrLn $ "P2: " ++ solveP2 contents
