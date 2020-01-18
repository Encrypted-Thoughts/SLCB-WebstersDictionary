using ScraperTool;
using System;
using System.Collections.Generic;

namespace ScraperTest
{
    class Program
    {
        static void Main(string[] args)
        {
            var html = $"https://www.merriam-webster.com/dictionary/encrypted";

            var paths = new List<string>
            {
                "//div[@id='definition-wrapper'][1]//div[@class='row entry-attr'][1]/div",
                "//div[@id='definition-wrapper'][1]//div[@id='dictionary-entry-1'][1]/div[@class='vg']"
            };

            var value = Scraper.Parse(html, paths);
            Console.WriteLine(value);
        }
    }
}
