import { Blockquote } from '@mantine/core';
import { InfoIcon } from '@phosphor-icons/react';
import type { Quote } from '../api/interfaces';

interface QuoteCardProps {
  quote: Quote;
}

export default function QuoteCard({ quote }: QuoteCardProps) {
  const icon = <InfoIcon />;
  return (
    <Blockquote
      color="blue"
      iconSize={38}
      cite={quote.description || undefined}
      icon={icon}
      mt="xl"
    >
      {quote.source}
    </Blockquote>
  );
}
