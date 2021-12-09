{- stack script --resolver lts-18.18 -}
import System.Environment
import Data.List

solve xs lag = genericLength . filter id  $ zipWith (>) (drop lag xs) xs

main = do
    args <- getArgs
    contents <- readFile $ head args
    let numbers = map (\x -> read x :: Integer) $ words contents
    putStrLn $ "Part 1: " ++ show (solve numbers 1)
    putStrLn $ "Part 2: " ++ show (solve numbers 3)
