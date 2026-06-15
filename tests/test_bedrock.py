from services.llm.bedrock_client import BedrockClient


def main() -> None:
    client = BedrockClient()

    response = client.converse(
        """
        Return ONLY valid JSON.

        {
          "ok": true
        }
        """
    )

    print(response)


if __name__ == "__main__":
    main()