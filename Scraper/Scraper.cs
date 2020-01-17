using HtmlAgilityPack;
using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Linq;
using System.Reflection;
using System.Collections;

namespace ScraperTool
{
    public static class Scraper
    {
        public static string Parse(string link, List<string> paths)
        {
            var web = new HtmlWeb();

            var htmlDoc = web.Load(link);

            var returns = new List<string>();
            foreach(var path in paths)
            {
                var node = htmlDoc.DocumentNode.SelectSingleNode(path);

                returns.Add(JsonConvert.SerializeObject(node, Formatting.None, new CustomJsonConverter()));
            }

            return $"[{string.Join(",", returns)}]";
        }
    }

    public class CustomJsonConverter : JsonConverter
    {

        public override bool CanConvert(Type objectType)
        {
            return true;
        }

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
        {
            throw new NotImplementedException();
        }

        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            if (!(value is HtmlNode)) return;

            var node = value as HtmlNode;

            var root = GetJson(node);

            root.WriteTo(writer);
        }

        private JObject GetJson(HtmlNode node)
        {
            var root = new JObject(new JProperty("name", node.Name), new JProperty("nodeType", node.NodeType.ToString()));

            var attributes = new JArray();
            foreach (var attribute in node.Attributes)
            {
                attributes.Add(new JObject(new JProperty(attribute.Name, attribute.Value)));
            }
            root.Add(new JProperty("attributes", attributes));

            var children = new JArray();
            foreach (var child in node.ChildNodes)
            {
                children.Add(GetJson(child));
            }
            root.Add(new JProperty("children", children));

            if (node.ChildNodes.Count == 0)
            {
                root.Add(new JProperty("innerText", node.InnerText));
            }

            return root;
        }
    }
}
