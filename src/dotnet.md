# .NET on Graviton
.NET is an open-source platform for writing different types of applications. Software engineers can write .NET based applications in multiple languages such as C#, F#, and Visual Basic. .NET applications are compiled into Common Intermediate Language (CIL). When an application is executed, the Common Language Runtime (CLR) loads that application binary and uses a just-in-time (JIT) compiler to generate machine code for the architecture being executed on. For more information, please see [what is .NET](https://dotnet.microsoft.com/learn/dotnet/what-is-dotnet).


## .NET Versions

Version            | Linux Arm32   | Linux Arm64   | Notes
------------------|-----------|-----------|-------------
.NET 9 | Yes | Yes | v9.0.0 released November 12, 2024 with Arm64 Linux builds. See also [Arm64 vectorization in .NET libraries](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-9/runtime#arm64-vectorization-in-net-libraries).
.NET 8 | Yes | Yes | v8.0.0 released November 14, 2023 with Arm64 Linux builds. See also [Arm64 Performance Improvements in .NET 8](https://devblogs.microsoft.com/dotnet/this-arm64-performance-in-dotnet-8/). For details on .NET 8 and Graviton, check out this blog: [Powering .NET 8 with AWS Graviton3: Benchmarks](https://aws.amazon.com/blogs/dotnet/powering-net-8-with-aws-graviton3-benchmarks/)
.NET 7 | Yes | Yes | v7.0.0 released November 8, 2022 with Arm64 Linux builds. For more details check out this video: [Boosting .NET application performance with Arm64 and AWS Graviton 3](https://www.youtube.com/watch?v=V4Lxs5TbaFk) Note that .NET 7 is [out of support](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core#lifecycle). 
[.NET 6](https://dotnet.microsoft.com/download/dotnet/6.0) | Yes | Yes |  V6.0.0 released November 8, 2021 with Arm64 Linux builds. For more details check out this blog: [.NET 6 on AWS](https://aws.amazon.com/blogs/developer/net-6-on-aws/) and video: [AWS re:Invent 2021 - Accelerate .NET 6 performance with Arm64 on AWS Graviton2](https://www.youtube.com/watch?v=iMlyZI9NhFw)
[.NET 5](https://dotnet.microsoft.com/download/dotnet/5.0) | Yes | Yes | Arm64-specific optimizations in the .NET libraries and the code produced by RyuJIT. [Arm64 Performance in .NET 5](https://devblogs.microsoft.com/dotnet/arm64-performance-in-net-5/). Note that .NET 5 is [out of support](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core#lifecycle). 
[.NET Framework 4.x](https://dotnet.microsoft.com/learn/dotnet/what-is-dotnet-framework) | No | No | The original implementation of the .NET Framework does not support Linux hosts, and Windows hosts are not suported on Graviton. 
[.NET Core 3.1](https://dotnet.microsoft.com/download/dotnet/3.1) | Yes | Yes | .NET Core 3.0 added support for [Arm64 for Linux](https://docs.microsoft.com/en-us/dotnet/core/whats-new/dotnet-core-3-0#linux-improvements). Note that .NET Core 3.1 is [out of support](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core#lifecycle).
[.NET Core 2.1](https://dotnet.microsoft.com/download/dotnet/2.1) | Yes* | No | Initial support was for [Arm32 was added to .NET Core 2.1](https://github.com/dotnet/announcements/issues/82). *Operating system support is limited, please see the [official documentation](https://github.com/dotnet/core/blob/main/release-notes/2.1/2.1-supported-os.md). Note that .NET Core 2.1 is [out of support](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core#lifecycle).


## .NET 5
With .NET 5 Microsoft has made specific Arm64 architecture optimizations. These optimizations were made in the .NET libraries as well as in the machine code output by the JIT process.

 * AWS DevOps Blog [Build and Deploy .NET web applications to ARM-powered AWS Graviton 2 Amazon ECS Clusters using AWS CDK](https://aws.amazon.com/blogs/devops/build-and-deploy-net-web-applications-to-arm-powered-aws-graviton-2-amazon-ecs-clusters-using-aws-cdk/)
 * AWS Compute Blog [Powering .NET 5 with AWS Graviton2: Benchmarks](https://aws.amazon.com/blogs/compute/powering-net-5-with-aws-graviton2-benchmark-results/) 
 * Microsoft .NET Blog [ARM64 Performance in .NET 5](https://devblogs.microsoft.com/dotnet/arm64-performance-in-net-5/)


## Building & Publishing for Linux Arm64
The .NET SDK supports choosing a [Runtime Identifier (RID)](https://docs.microsoft.com/en-us/dotnet/core/rid-catalog) used to target platforms where the applications run. These RIDs are used by .NET dependencies (NuGet packages) to represent platform-specific resources in NuGet packages. The following values are examples of RIDs: linux-arm64, linux-x64, ubuntu.14.04-x64, win7-x64, or osx.10.12-x64. For the NuGet packages with native dependencies, the RID designates on which platforms the package can be restored.

You can build and publish on any host operating system. As an example, you can develop on Windows and build locally to target Arm64, or you can use a CI server like Jenkins on Linux. The commands are the same.

```bash
dotnet build -r linux-arm64
dotnet publish -c Release -r linux-arm64
```

For more information about [publishing .NET apps with the .NET CLI](https://docs.microsoft.com/en-us/dotnet/core/deploying/deploy-with-cli) please see the offical documents.
