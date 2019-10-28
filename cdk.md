```csharp
namespace Hello
{
    public class HelloStack : Stack
    {
        public HelloStack(Construct parent, string id, IStackProps props) : base(parent, id, props)
        {
            new Bucket(this, "foo", new BucketProps()
            {
                BucketName = "foo-29837927493274234",
                RemovalPolicy=RemovalPolicy.DESTROY
            });
            new Table(this, "Items", new TableProps()
            {
                PartitionKey = new Attribute() { Name = "ItemId", Type = AttributeType.NUMBER },
                ReadCapacity = 10,
                WriteCapacity = 20,
                RemovalPolicy = RemovalPolicy.DESTROY
            });
        }
    }
}

```

```csharp

namespace Hello2
{
    class Program
    {
        static void Main(string[] args)
        {
            var app = new App(null);
            new Hello2Stack(app, "Hello2Stack", new StackProps()
            {
                Env = new Amazon.CDK.Environment()
                {
                    Region= "ap-northeast-1",
                    Account= "105964072553"
                }
            });
            app.Synth();
        }
    }
}

```


```csharp

using Amazon.CDK;
using Amazon.CDK.AWS.EC2;
namespace Hello2
{
    public class Hello2Stack : Stack
    {
        public Hello2Stack(Construct parent, string id, IStackProps props) : base(parent, id, props)
        {
            
            var defaultVpc = Vpc.FromLookup(this, "defaultvpc", new VpcLookupOptions()
            {
                IsDefault = true
            });
            for (int i = 0; i < 3; i++)
            {
                new Instance_(this, "webserver"+i, new InstanceProps()
                {
                    InstanceType = new InstanceType("t2.micro"),
                    MachineImage = new AmazonLinuxImage(),
                    Vpc = defaultVpc
                });

            }
        }
    }
}

```
